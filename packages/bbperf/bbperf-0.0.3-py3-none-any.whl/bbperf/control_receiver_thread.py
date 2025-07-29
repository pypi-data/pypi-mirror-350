# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time

from .exceptions import PeerDisconnectedException
from .udp_rate_manager_class import UdpRateManagerClass


# direction up, runs on client
# args are client args (not server args)
# falling off the end of this method terminates the process
def run_recv_term_queue(args, stdout_queue, control_conn, results_queue, shared_udp_sending_rate_pps):
    if args.verbosity:
        stdout_queue.put("starting control receiver process: run_recv_term_queue")

    udp_rate_manager = UdpRateManagerClass(args, shared_udp_sending_rate_pps)

    while True:

        try:
            # blocking
            bytes_read = control_conn.recv_a_c_block()

        except ConnectionResetError:
            if args.verbosity:
                stdout_queue.put("connection reset error")
            # exit process
            break

        except PeerDisconnectedException:
            if args.verbosity:
                stdout_queue.put("peer disconnected (control socket)")
            # exit process
            break

        received_str = bytes_read.decode()
        curr_time_str = str(time.time())
        new_str = received_str + curr_time_str + " d "

        results_queue.put(new_str)

        # udp autorate
        if args.udp and not args.bandwidth:
            udp_rate_manager.update(new_str)

    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting control receiver process: run_recv_term_queue")


# direction down, runs on server
# args are client args (not server args)
# falling off the end of this method terminates the process
def run_recv_term_send(args, stdout_queue, control_conn, shared_udp_sending_rate_pps):
    if args.verbosity:
        stdout_queue.put("starting control receiver process: run_recv_term_send")

    udp_rate_manager = UdpRateManagerClass(args, shared_udp_sending_rate_pps)

    while True:

        try:
            # blocking
            bytes_read = control_conn.recv_a_c_block()

        except ConnectionResetError:
            if args.verbosity:
                stdout_queue.put("connection reset error")
            # exit process
            break

        except PeerDisconnectedException:
            if args.verbosity:
                stdout_queue.put("peer disconnected (control socket)")
            # exit process
            break

        received_str = bytes_read.decode()
        curr_time_str = str(time.time())
        new_str = received_str + curr_time_str + " d "

        control_conn.send(new_str.encode())

        # udp autorate
        if args.udp and not args.bandwidth:
            udp_rate_manager.update(new_str)

    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting control receiver process: run_recv_term_send")


# direction down, runs on client (passthru)
# args are client args (not server args) -- this always runs on client
# falling off the end of this method terminates the process
def run_recv_queue(args, stdout_queue, control_conn, results_queue):
    if args.verbosity:
        stdout_queue.put("starting control receiver process: run_recv_queue")

    while True:
        try:
            # blocking
            bytes_read = control_conn.recv_a_d_block()

        except ConnectionResetError:
            if args.verbosity:
                stdout_queue.put("connection reset error")
            # exit process
            break

        except PeerDisconnectedException:
            if args.verbosity:
                stdout_queue.put("peer disconnected (control socket)")
            # exit process
            break

        received_str = bytes_read.decode()

        # passthru as is
        results_queue.put(received_str)

    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting control receiver process: run_recv_queue")
