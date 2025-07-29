# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time

from . import const


# We need to tell the server what our (the client's) address and port are for
# the udp test.  We do not know what is it (from the servers's perspective), so
# we send some traffic so the server can figure it out.

# falling off the end of this method terminates the process
def run(args, stdout_queue, data_sock, peer_addr):
    if args.verbosity:
        stdout_queue.put("data udp ping sender: start of process")

    peer_addr_for_udp = peer_addr

    payload_bytes = const.UDP_PING_MSG.encode()

    ping_interval_sec = 0.1
    ping_duration_sec = 5
    total_pings_to_send = ping_duration_sec / ping_interval_sec

    send_count = 0

    while True:

        try:
            data_sock.sendto(payload_bytes, peer_addr_for_udp)
            send_count += 1

        except Exception as e:
            stdout_queue.put("ERROR: data udp ping sender: exception: {}".format(e))
            # exit process
            break

        time.sleep(ping_interval_sec)

        if send_count > total_pings_to_send:
            break

    if args.verbosity:
        stdout_queue.put("data udp ping sender: end of process")
