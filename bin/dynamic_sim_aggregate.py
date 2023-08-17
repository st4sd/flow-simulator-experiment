#! /usr/bin/env python

# © Copyright IBM Corp. 2022 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import os
import tarfile

parser = argparse.ArgumentParser(description='Aggregate dynamic simulation results.')
parser.add_argument('--simulation_paths',
                    type=str,
                    action='store',
                    nargs='+',
                    metavar='SIMULATION_PATHS',
                    help='Simulation paths')
arg = parser.parse_args()

num_replicas = int(len(arg.simulation_paths)/3)

logs = tarfile.open("logs.tgz", "w:gz")
resume_files = tarfile.open("resume_files.tgz", "w:gz")

with tarfile.open("snapshots.tgz", "w:gz") as tar:
    for rep in range(num_replicas):
        axis = ["x", "y", "z"]
        idx = [rep, rep + num_replicas, rep + 2 * num_replicas]

        for ax, id in zip(axis, idx):
            file_path = f"{arg.simulation_paths[id]}/component_performance.csv"
            if os.path.exists(file_path):
                logs.add(file_path,
                         arcname=f"component_performance_{ax}_{str(rep).rjust(4, '0')}.csv")

            file_path = f"{arg.simulation_paths[id]}/out.stdout"
            logs.add(file_path, arcname=f"out_{ax}_{str(rep).rjust(4, '0')}.stdout")

            file_path = f"{arg.simulation_paths[id]}/resume.h5.tgz"
            if os.path.exists(file_path):
                resume_files.add(file_path, arcname=f"resume_{ax}_{str(rep).rjust(4, '0')}.tgz")

            tar.add(f"{arg.simulation_paths[id]}/snapshots",
                    arcname=f"snapshots_{ax}_{str(rep).rjust(4, '0')}", recursive=True)

logs.close()
resume_files.close()
