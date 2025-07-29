# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time
import socket
import select

from . import util
from . import const
from . import calibration


# falling off the end of this method terminates the process
def run(args, stdout_queue, data_sock, peer_addr, shared_udp_sending_rate_pps):
    if args.verbosity:
        stdout_queue.put("data sender: start of process")

    peer_addr_for_udp = peer_addr

    if args.udp and (peer_addr_for_udp is None):
        # for udp, we have to wait for a ping message so we know where to send the data packets
        while True:
            # blocking
            bytes_read, pkt_from_addr = data_sock.recvfrom(const.BUFSZ)
            if len(bytes_read) == len(const.UDP_PING_MSG):
                if bytes_read.decode() == const.UDP_PING_MSG:
                    peer_addr_for_udp = pkt_from_addr
                    if args.verbosity:
                        stdout_queue.put("data sender: peer address: {}".format(peer_addr_for_udp))
                    break

    # calculate sending rate

    if args.bandwidth or args.udp:
        if args.bandwidth:
            bandwidth_is_pps, bandwidth_val_int = util.convert_bandwidth_str_to_int(args.bandwidth)
        else:
            # must be UDP with no bandwidth specified, so use UDP autorate
            bandwidth_is_pps = True
            bandwidth_val_int = shared_udp_sending_rate_pps.value

        batch_size, delay_between_batches = util.convert_bandwidth_spec_to_batch_info(args, bandwidth_is_pps, bandwidth_val_int)

    # start sending

    if args.verbosity:
        stdout_queue.put("data sender: sending")

    curr_time_sec = time.time()

    # stop sending time
    end_time = curr_time_sec + args.time

    interval_start_time = curr_time_sec
    interval_end_time = interval_start_time + const.SAMPLE_INTERVAL_SEC

    interval_time_sec = 0.0
    interval_send_count = 0
    interval_bytes_sent = 0

    accum_send_count = 0
    accum_bytes_sent = 0

    total_send_counter = 1

    while True:
        curr_time_sec = time.time()
        is_calibrated = calibration.is_calibrated()
        record_type = b'run' if is_calibrated else b'cal'

        # we want to be fast here, since this is data write loop, so use ba.extend

        ba = bytearray()
        ba.extend(b' a ')
        ba.extend(record_type)
        ba.extend(b' ')
        ba.extend(str(curr_time_sec).encode())
        ba.extend(b' ')
        ba.extend(str(interval_time_sec).encode())
        ba.extend(b' ')
        ba.extend(str(interval_send_count).encode())
        ba.extend(b' ')
        ba.extend(str(interval_bytes_sent).encode())
        ba.extend(b' ')
        ba.extend(str(total_send_counter).encode())
        ba.extend(b' b ')

        if args.udp:
            ba.extend(const.PAYLOAD_1K)
        elif is_calibrated:
            ba.extend(const.PAYLOAD_4K)
        else:
            ba.extend(const.PAYLOAD_1K)

        try:
            # blocking
            # we want to block here, as blocked time should "count"

            # we use select to take advantage of tcp_notsent_lowat
            _, _, _ = select.select( [], [data_sock], [])

            if args.udp:
                num_bytes_sent = data_sock.sendto(ba, peer_addr_for_udp)
            else:
                # tcp
                num_bytes_sent = data_sock.send(ba)

            if num_bytes_sent <= 0:
                msg = "ERROR: send failed"
                stdout_queue.put(msg)
                raise Exception(msg)

        except ConnectionResetError:
            stdout_queue.put("Connection reset by peer")
            # exit process
            break

        except BrokenPipeError:
            # this can happen at the end of a tcp reverse test
            stdout_queue.put("broken pipe error")
            # exit process
            break

        except BlockingIOError:
            # same as EAGAIN EWOULDBLOCK
            # we did not send, loop back up and try again
            continue

        except socket.timeout:
            # we did not send, loop back up and try again
            continue

        total_send_counter += 1
        accum_send_count += 1
        accum_bytes_sent += num_bytes_sent

        if curr_time_sec > interval_end_time:
            interval_time_sec = curr_time_sec - interval_start_time
            interval_send_count = accum_send_count
            interval_bytes_sent = accum_bytes_sent

            if args.verbosity == 3:
                print("data_sender: a {} {} {} {} {} {} b".format(
                    record_type, curr_time_sec, interval_time_sec, interval_send_count, interval_bytes_sent, total_send_counter)
                )

            interval_start_time = curr_time_sec
            interval_end_time = interval_start_time + const.SAMPLE_INTERVAL_SEC
            accum_send_count = 0
            accum_bytes_sent = 0

            # update udp rate when autorate in effect
            if args.udp and not args.bandwidth:
                bandwidth_is_pps = True
                bandwidth_val_int = shared_udp_sending_rate_pps.value
                batch_size, delay_between_batches = util.convert_bandwidth_spec_to_batch_info(args, bandwidth_is_pps, bandwidth_val_int)

        # send very slowly at first to establish unloaded latency
        if not is_calibrated:
            time.sleep(0.2)
            # initialize batch variables here in case next loop is batch processing
            current_batch_start_time = time.time()
            current_batch_counter = 0
            continue

        # normal end of test
        if curr_time_sec > end_time:
            break

        if args.bandwidth or args.udp:
            current_batch_counter += 1
            if current_batch_counter >= batch_size:
                this_delay = delay_between_batches - (curr_time_sec - current_batch_start_time)
                if this_delay > 0:
                    time.sleep(delay_between_batches)
                current_batch_start_time += delay_between_batches
                current_batch_counter = 0


    util.done_with_socket(data_sock)

    if args.verbosity:
        stdout_queue.put("data sender: end of process")
