#!/usr/bin/python3

# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import multiprocessing
import time
import queue
import socket

from . import data_sender_thread
from . import data_udp_ping_sender_thread
from . import data_receiver_thread
from . import control_receiver_thread
from . import util
from . import calibration
from . import const
from . import output
from . import graph

from .tcp_control_connection_class import TcpControlConnectionClass


def client_mainline(args):
    if args.verbosity:
        print("args: {}".format(args))

    server_ip = args.client
    server_port = args.port

    data_conn_verification_str = "d" + const.SOFT_SECRET + " "

    # create control connection

    if args.verbosity:
        print("creating control connection")

    control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_sock.connect((server_ip, server_port))

    control_conn = TcpControlConnectionClass(control_sock)
    control_conn.set_args(args)

    control_conn.send_validation_string()

    if args.verbosity:

        print("created control connection")

    if args.verbosity:
        print("sending args to server {}".format(vars(args)))

    control_conn.send_args_to_server(args)

    if args.verbosity:
        print("sent args to server")

    # create data connection

    if args.verbosity:
        print("creating data connection")

    if args.udp:
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data_sock.settimeout(const.SOCKET_TIMEOUT_SEC)

    else:
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.connect((server_ip, server_port))
        data_sock.settimeout(const.SOCKET_TIMEOUT_SEC)

        # send verification string
        num_bytes_sent = data_sock.send(data_conn_verification_str.encode())
        if num_bytes_sent != len(data_conn_verification_str):
            raise Exception("ERROR: send failed")

    server_addr = (server_ip, server_port)

    if args.verbosity:
        print("created data connection ({})".format("udp" if args.udp else "tcp"))

    shared_udp_sending_rate_pps = multiprocessing.Value('d', const.UDP_DEFAULT_INITIAL_RATE)

    # run test

    if args.verbosity:
        print("test running")

    calibration.start()

    if not args.reverse:
        # up direction

        control_receiver_stdout_queue = multiprocessing.Queue()
        control_receiver_results_queue = multiprocessing.Queue()

        control_receiver_process = multiprocessing.Process(
            name = "controlreceiver",
            target = control_receiver_thread.run_recv_term_queue,
            args = (args, control_receiver_stdout_queue, control_conn, control_receiver_results_queue, shared_udp_sending_rate_pps),
            daemon = True)

        control_receiver_process.start()

        data_sender_stdout_queue = multiprocessing.Queue()

        data_sender_process = multiprocessing.Process(
            name = "datasender",
            target = data_sender_thread.run,
            args = (args, data_sender_stdout_queue, data_sock, server_addr, shared_udp_sending_rate_pps),
            daemon = True)

        # test starts here
        data_sender_process.start()

        thread_list = []
        thread_list.append(control_receiver_process)
        thread_list.append(data_sender_process)

        queue_list = []
        queue_list.append([control_receiver_results_queue, output.print_output])
        queue_list.append([control_receiver_stdout_queue, print])
        queue_list.append([data_sender_stdout_queue, print])

    if args.reverse:
        # down direction

        # udp pinger
        if args.udp:
            data_udp_ping_sender_stdout_queue = multiprocessing.Queue()

            data_udp_ping_sender_process = multiprocessing.Process(
                name = "dataudppingsender",
                target = data_udp_ping_sender_thread.run,
                args = (args, data_udp_ping_sender_stdout_queue, data_sock, server_addr),
                daemon = True)

            data_udp_ping_sender_process.start()

            # yield to let the first ping fly
            time.sleep(0.005)

        data_receiver_stdout_queue = multiprocessing.Queue()

        data_receiver_process = multiprocessing.Process(
            name = "datareceiver",
            target = data_receiver_thread.run,
            args = (args, data_receiver_stdout_queue, control_conn, data_sock, server_addr),
            daemon = True)

        data_receiver_process.start()

        control_receiver_stdout_queue = multiprocessing.Queue()
        control_receiver_results_queue = multiprocessing.Queue()

        control_receiver_process = multiprocessing.Process(
            name = "controlreceiver",
            target = control_receiver_thread.run_recv_queue,
            args = (args, control_receiver_stdout_queue, control_conn, control_receiver_results_queue),
            daemon = True)

        control_receiver_process.start()

        # test starts here

        control_conn.send_start_message_to_server()

        thread_list = []
        thread_list.append(data_receiver_process)
        thread_list.append(control_receiver_process)
        if args.udp:
            thread_list.append(data_udp_ping_sender_process)

        queue_list = []
        if args.udp:
            queue_list.append([data_udp_ping_sender_stdout_queue, print])
        queue_list.append([data_receiver_stdout_queue, print])
        queue_list.append([control_receiver_stdout_queue, print])
        queue_list.append([control_receiver_results_queue, output.print_output])


    # output loop

    output.init(args)

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

        # exit program
        break

    output.term()

    util.done_with_socket(data_sock)
    control_conn.close()

    graphdatafilename = output.get_graph_data_file_name()
    rawdatafilename = output.get_raw_data_file_name()

    if args.graph:
        graph.create_graph(args, graphdatafilename)
        print("created graph: {}".format(graphdatafilename + ".png"))

    if args.keep:
        print("keeping graph data file: {}".format(graphdatafilename))
        print("keeping raw data file: {}".format(rawdatafilename))
    else:
        output.delete_data_files()
