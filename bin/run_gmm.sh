#!/bin/bash

# © Copyright IBM Corp. 2023 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

while getopts c:b:f: flag
do
    case "${flag}" in
        c) Centerlines=${OPTARG};;
        b) BinaryImage=${OPTARG};;
        f) CosFolder=${OPTARG};;
    esac
done

ln -s ${CosFolder}/${Centerlines}.json ./${Centerlines}.json

ln -s /root/simulator/gmm ./gmm
ln -s /root/simulator/bin ./bin
ln -s /root/simulator/util ./util

BinaryImagePath="${CosFolder}/${BinaryImage}.raw"

if [ -f ${BinaryImagePath} ];
then
    ln -s ${BinaryImagePath} ./${BinaryImage}.raw
    gmm.py --case_folder . --case_filename case_input --centerlines_filename ${Centerlines} --binary_image_filename ${BinaryImage} --print_progress .
else
    gmm.py --case_folder . --case_filename case_input --centerlines_filename ${Centerlines} --print_progress .
fi

echo "FINISHED"
