# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time

from . import const


calibration_start_time = None
calibration_end_time = None
min_rtt_sec = None


def start():
    global calibration_start_time
    global calibration_end_time

    calibration_start_time = time.time()
    calibration_end_time = calibration_start_time + const.UNLOADED_DURATION_SEC

def is_calibrated():
    if calibration_end_time is None:
        return False

    if time.time() < calibration_end_time:
        return False

    return True

def update_rtt_sec(new_sample):
    global min_rtt_sec

    if (min_rtt_sec is None) or (new_sample < min_rtt_sec):
        min_rtt_sec = new_sample

def get_unloaded_latency_rtt_sec():
    if min_rtt_sec is None:
        raise Exception("ERROR: there is no min rtt")

    return min_rtt_sec
