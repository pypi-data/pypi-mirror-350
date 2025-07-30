#!/bin/bash

# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

SERVER_ADDR=127.0.0.1

DURATION=10

OPTARGS=""
#OPTARGS="-k -g"

set -x

bbperf -c $SERVER_ADDR -t $DURATION $EXTRAARGS

bbperf -c $SERVER_ADDR -t $DURATION $EXTRAARGS -R

bbperf -c $SERVER_ADDR -t $DURATION $EXTRAARGS -u -t 20

bbperf -c $SERVER_ADDR -t $DURATION $EXTRAARGS -u -R -t 20

bbperf -c $SERVER_ADDR -t $DURATION $EXTRAARGS -J /tmp/foo578439759837.out
rm /tmp/foo578439759837.out

