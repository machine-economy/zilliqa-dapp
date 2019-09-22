#!/bin/bash
#
# This file is part of Machine Economy Zilliqa Dapp Project.
#
# Copyright (c) 2019 Rustiq Technology Ltd & Well Bred Software Ltd
# MIT License

function kill_at_port {
    PID=`lsof -t -i:${1}`
    if [ "$PID" != "" ]; then
        echo Killing pid $PID at port $1
	kill -9 $PID
    else
        echo Nothing to kill at port $1
    fi
}

# Kill the Kaya instance.
kill_at_port 4200
# Remove runtime files.
rm -rf ./runtime-data
