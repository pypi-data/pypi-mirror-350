#!/usr/bin/python3

# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time
import socket
import multiprocessing
import queue

from . import data_sender_thread
from . import data_receiver_thread
from . import control_receiver_thread
from . import util
from . import const
from . import calibration

from .tcp_control_connection_class import TcpControlConnectionClass


def server_mainline(args):
    server_port = args.port

    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_sock.bind(('0.0.0.0', server_port))

    listen_sock.listen(32)          # listen backlog
    listen_sock.setblocking(True)

    server_port = listen_sock.getsockname()[1]

    while True:
        print("server listening on port ", server_port)

        data_conn_verification_str = "d" + const.SOFT_SECRET + " "

        # accept control connection

        # blocking
        control_sock, _ = listen_sock.accept()

        control_conn = TcpControlConnectionClass(control_sock)
        control_conn.set_args(args)

        print("client connected (control socket)")

        control_conn.recv_and_check_validation_string()

        print("waiting for args from client")

        # blocking
        client_args = control_conn.receive_args_from_client()

        if client_args.verbosity:
            print("received args from client: {}".format(vars(client_args)))
        else:
            print("received args from client")

        control_conn.set_args(client_args)

        # accept data connection

        if client_args.udp:

            if client_args.verbosity:
                print("creating data connection (udp)")

            data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data_sock.bind(("0.0.0.0", server_port))

        else:

            if client_args.verbosity:
                print("creating data connection (tcp)")

            # blocking
            data_sock, _ = listen_sock.accept()

        data_sock.settimeout(const.SOCKET_TIMEOUT_SEC)

        # perform verification of data connection
        if not client_args.udp:
            # blocking
            total_num_bytes_to_read = len(data_conn_verification_str)
            payload_bytes = util.recv_exact_num_bytes_tcp(data_sock, total_num_bytes_to_read)
            payload_str = payload_bytes.decode()
            if payload_str != data_conn_verification_str:
                raise Exception("ERROR: client connection invalid, ident: {} payload {}".format(data_conn_verification_str[0], payload_str))

        print("created data connection ({})".format("udp" if client_args.udp else "tcp"))

        shared_udp_sending_rate_pps = multiprocessing.Value('d', const.UDP_DEFAULT_INITIAL_RATE)

        # run test

        print("test running")

        calibration.start()

        if not client_args.reverse:
            # direction up

            data_receiver_stdout_queue = multiprocessing.Queue()

            client_addr = None

            data_receiver_process = multiprocessing.Process(
                name = "datareceiver",
                target = data_receiver_thread.run,
                args = (client_args, data_receiver_stdout_queue, control_conn, data_sock, client_addr),
                daemon = True)

            data_receiver_process.start()

            thread_list = []
            thread_list.append(data_receiver_process)

            queue_list = []
            queue_list.append([data_receiver_stdout_queue, print])

        if client_args.reverse:
            # direction down

            control_receiver_stdout_queue = multiprocessing.Queue()

            control_receiver_process = multiprocessing.Process(
                name = "controlreceiver",
                target = control_receiver_thread.run_recv_term_send,
                args = (client_args, control_receiver_stdout_queue, control_conn, shared_udp_sending_rate_pps),
                daemon = True)

            data_sender_stdout_queue = multiprocessing.Queue()

            data_sender_process = multiprocessing.Process(
                name = "datasender",
                target = data_sender_thread.run,
                args = (client_args, data_sender_stdout_queue, data_sock, None, shared_udp_sending_rate_pps),
                daemon = True)

            # wait for start message
            control_conn.wait_for_start_message()

            control_receiver_process.start()

            data_sender_process.start()

            thread_list = []
            thread_list.append(control_receiver_process)
            thread_list.append(data_sender_process)

            queue_list = []
            queue_list.append([control_receiver_stdout_queue, print])
            queue_list.append([data_sender_stdout_queue, print])

        # both up and down

        while True:
            queue_was_processed = False

            for queue_to_read, function_to_call in queue_list:
                try:
                    s1 = queue_to_read.get_nowait()
                    queue_was_processed = True
                    function_to_call(s1)
                except queue.Empty:
                    pass

            if queue_was_processed:
                # immediately loop again
                continue

            if util.threads_are_running(thread_list):
                # nothing in queues, but test is still running
                time.sleep(0.01)
                continue

            # nothing in queues, and test has ended
            break

        util.done_with_socket(data_sock)
        control_conn.close()

        print("client ended")
