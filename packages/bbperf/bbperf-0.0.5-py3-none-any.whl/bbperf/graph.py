# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import os
import argparse
import subprocess


def create_graph(args, datafile1):

    this_script_dir = os.path.dirname(os.path.abspath(__file__))

    if args.udp:
        gp_file = this_script_dir + "/udp-graph.gp"
    else:
        gp_file = this_script_dir + "/tcp-graph.gp"

    gnuplot_script = "datafile1 = \"" + datafile1 + "\" ; load \"" + gp_file + "\""

    result = subprocess.run(["gnuplot", "-e", gnuplot_script], capture_output=True)

    if args.verbosity or (result.returncode != 0):
        print("gnuplot -e {}".format(gnuplot_script))
        print("returncode: {}".format(result.returncode))
        print("stdout: {}".format(result.stdout))
        print("stderr: {}".format(result.stderr))


if __name__ == '__main__':
    datafile1 = "/tmp/bbperf-tcp-data-aa97m9xl"

    args_d = { "udp": True }

    # recreate args as if it came directly from argparse
    args = argparse.Namespace(**args_d)

    create_graph(args, datafile1)
