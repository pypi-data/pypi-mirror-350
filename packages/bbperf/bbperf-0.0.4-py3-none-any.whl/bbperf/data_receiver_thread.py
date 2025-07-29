# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time
import socket

from . import const
from . import util

# args are client args
def run(args, stdout_queue, control_conn, data_sock, peer_addr):

    if args.verbosity:
        stdout_queue.put("starting data receiver process")

    # do not block on the below recv calls as we want to exit the process when
    # the "end of run" timer expires even if the flow of packets has stopped
    data_sock.settimeout(0.05)

    peer_addr_for_udp = peer_addr

    end_time = None

    total_recv_calls = 0

    interval_start_time = time.time()
    interval_end_time = interval_start_time + const.SAMPLE_INTERVAL_SEC

    interval_pkts_received = 0
    interval_bytes_received = 0

    # do until end of test duration
    # we will not get a connection close with udp
    while True:

        try:
            num_bytes_read = 0
            if args.udp:
                # recv with timeout
                bytes_read, pkt_from_addr = data_sock.recvfrom(const.BUFSZ)

                # validate peer address
                # all subsequent packets should come from the same addr as the first one
                if pkt_from_addr != peer_addr_for_udp:
                    if peer_addr_for_udp is None:
                        # first packet is received
                        peer_addr_for_udp = pkt_from_addr
                        if not args.quiet:
                            print("peer address: {}".format(peer_addr_for_udp))
                    else:
                        raise Exception("ERROR: datagram from wrong peer address")

                num_bytes_read = len(bytes_read)

            else:
                # tcp
                # recv with timeout
                bytes_read = data_sock.recv(const.BUFSZ)

                num_bytes_read = len(bytes_read)

                if num_bytes_read == 0:
                    # peer has disconnected
                    if args.verbosity:
                        stdout_queue.put("peer disconnected (data socket)")
                    # exit process
                    break

        except socket.timeout:
            pass

        curr_time_sec = time.time()

        if end_time and (curr_time_sec > end_time):
            if args.verbosity:
                stdout_queue.put("data receiver thread: end of test, exiting")
            # exit process
            break

        if num_bytes_read == 0:
            # recv must have timed out, skip the rest of this loop
            continue

        total_recv_calls += 1

        if not end_time:
            # first data packet arrived, so test just started running
            end_time = curr_time_sec + args.time

        interval_pkts_received += 1                     # valid for udp only
        interval_bytes_received += num_bytes_read

        if curr_time_sec > interval_end_time:
            interval_time_sec = curr_time_sec - interval_start_time

            # find the packet send time in the user payload

            a_b_block = None

            idx_of_a = bytes_read.find(b' a ')
            if idx_of_a > -1:
                idx_of_b = bytes_read.find(b' b ', idx_of_a)
                if idx_of_b > -1:
                    a_b_block = bytes_read[ idx_of_a : idx_of_b + 3 ]

            if a_b_block is None:
                # skip sending for this packet, but stay "in" sample interval
                continue

            # sending info back to client on control connection

            ba = bytearray()
            ba.extend(a_b_block)
            ba.extend(str(interval_time_sec).encode())
            ba.extend(b' ')
            ba.extend(str(interval_pkts_received).encode())
            ba.extend(b' ')
            ba.extend(str(interval_bytes_received).encode())
            ba.extend(b' ')
            ba.extend(str(total_recv_calls).encode())       # num of pkts received, valid for udp only
            ba.extend(b' c ')

            try:
                control_conn.send(ba)

            except Exception:
                stdout_queue.put("ERROR: send on control socket failed 2")
                # exit process
                break

            interval_bytes_received = 0
            interval_pkts_received = 0

            interval_start_time = curr_time_sec
            interval_end_time = interval_start_time + const.SAMPLE_INTERVAL_SEC


    # peer disconnected (or an error)
    util.done_with_socket(data_sock)
    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting data receiver process")
