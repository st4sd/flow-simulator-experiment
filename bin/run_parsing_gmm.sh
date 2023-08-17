#!/bin/bash

# © Copyright IBM Corp. 2023 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

while getopts i: flag
do
    case "${flag}" in
        i) CaseInputFolder=${OPTARG};;
    esac
done

ln -s ${CaseInputFolder} ./case_input

parse_gmm_parameters.py --case_folder . --case_filename case_input --print_progress .

echo "FINISHED"
