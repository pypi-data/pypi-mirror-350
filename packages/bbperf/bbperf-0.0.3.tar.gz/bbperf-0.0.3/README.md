<p align="center"><strong>bbperf</strong> <em>- An end-to-end performance and bufferbloat measurement tool</em></p>

`bbperf` measures the following for both TCP and UDP:

* End-to-end latency, both unloaded and loaded
* Throughput
* Bandwidth Delay Product (BDP)
* Usage of buffers between the endpoints
* Bufferbloat (when the usage of buffers is excessive)

For UDP, it also measures:

* Packet rates
* Packet loss rates

Features that distinguish this tool from existing tools include:

* Latency, both unloaded and loaded, is measured by the same flow that is under test.

    Other tools will commonly measure latency using a different flow or different protocol.  One of the reasons why using different protocols and/or different flows is not desirable is because fair queuing will cause the latency of those other flows to be much lower (better) than the flow that matters.

* Bufferbloat is calculated

    It is often assumed that TCP receive buffers are the only source of bufferbloat.  While that is common, it misses many other locations where bufferbloat may occur.  This tool reports the effects of all sources of bufferbloat, not just TCP receive buffers.

* Automatic generation of graphs

* The UDP option will automatically adjust the sending rate to just above the goodput rate so that any bufferbloat issues are measured.  This feature is enabled by default.  Simply omit the `-b/--bandwidth` option when running a `-u/--udp` test.

### Usage

To run a test:

1. Start the server on one host
```
    $ bbperf.py -s
```

2. Run the client on another host
```
    $ bbperf.py -c <ip address of server> [additional options as desired]
```

`bbperf` will use port 5301 between the client and server (by default).

The first 5 seconds performs a calibration, during which it captures the unloaded latency between endpoints.

The direction of data flow is from the client to the server.  That is reversed when the "-R" option is specified.

```
$ bbperf.py --help
usage: bbperf.py [-h] [-v] [-s] [-c SERVER_IP] [-p SERVER_PORT] [-R] [-t SECONDS] [-u] [-b BANDWIDTH] [-g] [-k] [-J JSON_FILE]

bbperf: end to end performance and bufferbloat measurement tool

options:
  -h, --help            show this help message and exit
  -v, --verbosity       increase output verbosity
  -s, --server          run in server mode
  -c, --client SERVER_IP
                        run in client mode
  -p, --port SERVER_PORT
                        server port (default: 5301)
  -R, --reverse         data flow in download direction (server to client)
  -t, --time SECONDS    duration of run in seconds
  -u, --udp             run in UDP mode (default: TCP mode)
  -b, --bandwidth BANDWIDTH
                        n[kmgKMG] | n[kmgKMG]pps, optional for both TCP and UDP
  -g, --graph           generate graph (requires gnuplot)
  -k, --keep            keep data file
  -J, --json-file JSON_FILE
                        JSON output file
```

Output from `bbperf` includes the following information:
```
    sent_time       time when a packet was sent
    recv_time       time when a packet was received
    sender_pps      packets per second sent
    sender_Mbps     bits per second sent
    receiver_pps    packets per second received
    receiver_Mbps   bits per second received
    unloaded_rtt_ms unloaded RTT in milliseconds (determined during calibration)
    rtt_ms          RTT in milliseconds
    BDP_bytes       Calculated BDP in bytes
    buffered_bytes  Actual bytes in flight
    bloat           Ratio of buffered bytes to BDP
    pkts_dropped    number of packets dropped (UDP only)
    drop%           percentage of packets dropped (UDP only)
```

### Installation

`bbperf` is available via PyPI repository (pypi.org) and can be installed using pip.

```
python3 -m venv bbperf-venv
. bbperf-venv/bin/active
pip install bbperf

bbperf.py [options]
```

In the event python3 is not already installed on the host:

```
apt-get install python3 python3-pip  (Debian/Ubuntu)
dnf install python3 python3-pip      (Fedora/RHEL)
```

---
Copyright (c) 2024 Cloudflare, Inc.<br/>
Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

