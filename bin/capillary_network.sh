#!/bin/bash

# © Copyright IBM Corp. 2022 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

while getopts r:v:c:s:f: flag
do
    case "${flag}" in
        r) replica=${OPTARG};;
        v) voxel_size=${OPTARG};;
        c) capillary_length=${OPTARG};;
        s) sample_size=${OPTARG};;
        f) sample_file=${OPTARG};;
    esac
done

capillary_network.py . --replica_number ${replica} --voxel_size ${voxel_size} --capillary_length ${capillary_length} --sample_size ${sample_size},${sample_size},${sample_size} --filename ${sample_file}
