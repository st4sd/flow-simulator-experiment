#! /usr/bin/env python

# © Copyright IBM Corp. 2022 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import tarfile

import h5py
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generates 2D or 3D network from the centerline.')
parser.add_argument('--result_files_paths',
                    action='store',
                    required=True,
                    nargs='+',
                    metavar='RESULT_FILES_PATHS',
                    help='Static files results paths.')
parser.add_argument('--capillary_data_files_paths',
                    action='store',
                    required=True,
                    nargs='+',
                    metavar='CAPILLARY_DATA_FILES_PATHS',
                    help='Capillary data files paths.')
parser.add_argument('--centerlines_files_paths',
                    action='store',
                    required=True,
                    nargs='+',
                    metavar='CENTERLINES_FILES_PATHS',
                    help='Centerlines files paths.')
arg = parser.parse_args()

static_results = arg.result_files_paths
capillary_data = arg.capillary_data_files_paths
centerlines_json = arg.centerlines_files_paths

num_replicas = int(len(arg.result_files_paths)/3)

tar = tarfile.open("centerlines.tar", "w")

with open("permeability_out.csv", "a") as file_permeability:
    file_permeability.write("REPLICA,POROSITY,NODES,LINKS,NX,NY,NZ,KX(mD),KY(mD),KZ(mD)\n")

    for rep in range(num_replicas):

        K = np.zeros(3, dtype=float)

        with open(capillary_data[rep], "r") as file:
            cap_data = file.read()

        with h5py.File(static_results[rep], "r") as file:
            K[0] = np.squeeze(np.array(file["permeability_x"], dtype=float))*1.01325e15

        with h5py.File(static_results[rep + num_replicas], "r") as file:
            K[1] = np.squeeze(np.array(file["permeability_y"], dtype=float))*1.01325e15

        with h5py.File(static_results[rep + 2 * num_replicas], "r") as file:
            K[2] = np.squeeze(np.array(file["permeability_z"], dtype=float))*1.01325e15

        file_permeability.write(f"{cap_data},{str(K[0])},{str(K[1])},{str(K[2])}\n")

        tar.add(centerlines_json[rep], arcname=f"centerlines_{str(rep).rjust(4, '0')}.json",
                recursive=False)

tar.close()
