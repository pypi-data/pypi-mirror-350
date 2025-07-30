<p align="center"><strong>bbperf</strong> <em>- An end-to-end performance and bufferbloat measurement tool</em></p>

`bbperf` measures what matters most.

Traditional network performance measurement tools collect metrics such as latency and throughput regardless of the conditions that exist during the collection period.  While valuable for many uses, that approach can miss reporting the actual performance that real user payloads experience on production networks.  This tool only reports performance metrics when the flow is operating at "max buffer usage".  Max buffer usage is when the active flow has filled any and all buffers that exist along the packet path between the endpoints.

User payload is used to measure latency and throughput.  This accounts for the performance impact of transparent proxies, transparent tunnels, transparent firewalls, and all the other things that are not visible to the endpoints.  It also simplifies the interpretation of retransmissions on user performance, which is non-intuitive at best.  This is because some retransmissions are due to the real loss of user payload while many are not.  In this tool, the loss of user payload will show up in the latency and throughput metrics, i.e. higher latencies and lower throughput.

Features:

* Latency, both unloaded and loaded, is measured by the same flow that is under test.

    Other tools will commonly measure latency using a different flow or different protocol.  One of the reasons why using different protocols and/or different flows is not desirable is because fair queuing will cause the latency of those other flows to be much lower (better) than the flow that matters.

* Throughput

    Both sender and receiver rates are collected, but the receiver rate (a.k.a. goodput) is the important one.

* Bufferbloat is calculated

    It is often assumed that TCP receive buffers are the only source of bufferbloat.  While that is common, it misses many other locations where bufferbloat may occur.  This tool reports the effects of all sources of bufferbloat, not just TCP receive buffers.

    `bbperf` calculates both the BDP (bandwidth delay product) and the total amount of buffer actually used.  The difference between those two is reported as "excess buffer usage".  A small number for this metric is normal and expected, but a large number, relative to BDP, is bufferbloat.  Bufferbloat also appears as a large difference between unloaded and loaded latency.

* Both TCP and UDP are supported

    Both benchmark tests will wait until it has reached "max buffer usage" before collecting metrics data.  For TCP, it will wait for the sending and receiving rates to match.  For UDP, the sending rate will be automatically adjusted to be just above the maximum packet rate without dropping packets before starting its metrics collection.

* `bbperf` measures the performance of data flow in one direction only.

    Network routing can be asymmetric, bottleneck links are asymmetric, bufferbloat is asymmetric, all of which means that performance is asymmetric.  `bbperf` allows us to see the asymmetry.

    Data flow in `bbperf` is one way.  The direction of data flow is from the client host to the server host (unless the `-R` option is specified).  That is the direction being measured, and is what is reported in the metrics.

    Latency is measured round trip, but the return traffic (from the data receiver back to the data sender) is low-volume and should not contribute any bufferbloat-related latency to the measurement.  This cannot be guaranteed, in the same way that it cannot be guaranteed that the unloaded latency measurement does not contain any bufferbloat-induced latency.  But it does ensure that no bufferbloat-induced latency is cause by `bbperf`s own flow.

* Automatic generation of graphs

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
usage: bbperf.py [-h] [-v] [-q] [-s] [-c SERVER_IP] [-p SERVER_PORT] [-R] [-t SECONDS] [-u] [-g] [-k] [-J JSON_FILE]

bbperf: end to end performance and bufferbloat measurement tool

options:
  -h, --help            show this help message and exit
  -v, --verbosity       increase output verbosity (can be repeated)
  -q, --quiet           decrease output verbosity (can be repeated)
  -s, --server          run in server mode
  -c, --client SERVER_IP
                        run in client mode
  -p, --port SERVER_PORT
                        server port (default: 5301)
  -R, --reverse         data flow in download direction (server to client)
  -t, --time SECONDS    duration of run in seconds
  -u, --udp             run in UDP mode (default: TCP mode)
  -g, --graph           generate graph (requires gnuplot on the client host)
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

Output to standard out is controlled via the `--verbosity` and `--quiet` options as follows:
```
    -qq           nothing to stdout except errors
    -q            run summary in json format
(neither option)  progress update once per second plus run summary in json format (default)
    -v            progress update once per 0.1 seconds, additional output, and run summary in json format
    -vv           debugging info useful for developers only
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

