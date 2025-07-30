# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

# defaults
SERVER_PORT = 5301
DURATION_SEC = 10
UNLOADED_DURATION_SEC=5

# for socket recv()
BUFSZ = 4096

PAYLOAD_1K = b'a'*1024
PAYLOAD_4K = b'a'*4096

SOFT_SECRET = "ZZ32gkogidrueowiruvnmxn432874ZZ"

# sample interval time
SAMPLE_INTERVAL_SEC = 0.1
STDOUT_INTERVAL_SEC = 1

RATE_LIMITED_BATCH_SIZE_PKTS_UDP_PKTS = 20
RATE_LIMITED_BATCH_SIZE_PKTS_TCP_PKTS = 5

START_MSG = " start "
UDP_PING_MSG = "ping"

SOCKET_TIMEOUT_SEC=20

UDP_DEFAULT_INITIAL_RATE = 8000

UDP_MIN_RATE = 100
UDP_MAX_RATE = 800000
