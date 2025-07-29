# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import json
import argparse
import socket

from . import const
from . import util
from .exceptions import PeerDisconnectedException


class TcpControlConnectionClass:

    # class variables

    validation_str = "c" + const.SOFT_SECRET + " "


    def __init__(self, control_sock):
        self.control_sock = control_sock
        self.args = None

        self.read_buffer = bytearray()

        control_sock.settimeout(const.SOCKET_TIMEOUT_SEC)

        # set TCP_NODELAY because the control messages back to the
        # sender from the data receiver are part of the RTT measurement
        control_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def set_args(self, args):
        self.args = args


    def send(self, payload_bytes):

        num_bytes_sent = self.control_sock.send(payload_bytes)

        num_payload_bytes = len(payload_bytes)

        if num_bytes_sent != num_payload_bytes:
            raise Exception("ERROR: send failed: wrong number of bytes sent: expected {}, actual {}".format(
                num_payload_bytes,
                num_bytes_sent
            ))

        if self.args and self.args.verbosity == 3:
            print("control connection: send: {}".format(payload_bytes.decode()))


    def send_validation_string(self):
        self.send(self.validation_str.encode())


    def send_args_to_server(self, args):
        args_json = json.dumps(vars(args))
        self.send(args_json.encode())


    def send_start_message_to_server(self):
        if self.args.verbosity:
            print("sending start message")

        self.send(const.START_MSG.encode())


    def recv(self, num_bytes_to_read):

        # blocking
        recv_bytes = self.control_sock.recv(num_bytes_to_read)

        if len(recv_bytes) == 0:
            raise PeerDisconnectedException()

        if self.args and self.args.verbosity == 3:
            print("control connection: recv: {}".format(recv_bytes.decode()))

        return recv_bytes


    def recv_into_buffer_until_minimum_size(self, minimum_buffer_size):

        while True:
            if len(self.read_buffer) >= minimum_buffer_size:
                break

            num_bytes_remaining = minimum_buffer_size - len(self.read_buffer)

            # blocking
            recv_bytes = self.recv(num_bytes_remaining)

            self.read_buffer.extend(recv_bytes)


    def recv_into_buffer_until_substr_found(self, substr_bytes):

        while True:

            substr_idx = self.read_buffer.find(substr_bytes)
            if substr_idx > -1:
                # found
                break

            # blocking
            recv_bytes = self.recv(const.BUFSZ)

            self.read_buffer.extend(recv_bytes)

        return substr_idx


    def recv_and_check_validation_string(self):
        len_str = len(self.validation_str)

        self.recv_into_buffer_until_minimum_size(len_str)

        received_bytes = self.read_buffer[ 0 : len_str ]
        self.read_buffer = self.read_buffer[ len_str : ]

        received_str = received_bytes.decode()

        if received_str != self.validation_str:
            raise Exception("ERROR: client connection invalid, ident: {} payload {}".format(self.validation_str[0], received_str))


    def receive_args_from_client(self):
        # starts with "{" and ends with "}"

        # blocking
        substr_idx = self.recv_into_buffer_until_substr_found(b'}')

        received_bytes = self.read_buffer[ 0 : substr_idx + 1 ]
        self.read_buffer = self.read_buffer[ substr_idx + 1 : ]

        received_str = received_bytes.decode()

        args_d = json.loads(received_str)

        # recreate args as if it came directly from argparse
        args = argparse.Namespace(**args_d)

        return args


    def wait_for_start_message(self):
        if self.args.verbosity:
            print("waiting for start message")

        len_str = len(const.START_MSG)

        # blocking
        self.recv_into_buffer_until_minimum_size(len_str)

        received_bytes = self.read_buffer[ 0 : len_str ]
        self.read_buffer = self.read_buffer[ len_str : ]

        received_str = received_bytes.decode()

        if received_str != const.START_MSG:
            raise Exception("ERROR: failed to receive start message")

        if self.args.verbosity:
            print("received start message")


    def recv_a_c_block(self):
        start_bytes = b' a '
        end_bytes = b' c '

        # blocking
        substr_idx = self.recv_into_buffer_until_substr_found(end_bytes)

        received_bytes = self.read_buffer[ 0 : substr_idx + 3 ]
        self.read_buffer = self.read_buffer[ substr_idx + 3 : ]

        if not (received_bytes.startswith(start_bytes) and received_bytes.endswith(end_bytes)):
            raise Exception("recv_a_c_block failed")

        return received_bytes


    def recv_a_d_block(self):
        start_bytes = b' a '
        end_bytes = b' d '

        # blocking
        substr_idx = self.recv_into_buffer_until_substr_found(end_bytes)

        received_bytes = self.read_buffer[ 0 : substr_idx + 3 ]
        self.read_buffer = self.read_buffer[ substr_idx + 3 : ]

        if not (received_bytes.startswith(start_bytes) and received_bytes.endswith(end_bytes)):
            raise Exception("recv_a_d_block failed")

        return received_bytes


    def close(self):
        util.done_with_socket(self.control_sock)
