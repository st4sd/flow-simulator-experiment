#!/bin/bash

# © Copyright IBM Corp. 2022 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

while getopts a: flag
do
    case "${flag}" in
        a) axis=${OPTARG};;
    esac
done

ln -s /root/simulator/util ./util
mkdir snapshots
flow-simulator.x --run_simulation config_${axis}.json