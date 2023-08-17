#!/usr/bin/env python3

# © Copyright IBM Corp. 2022 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import json
import numpy as np


parser = argparse.ArgumentParser(description='Generates a config file from a centerline an run a \
    static simulation.')
parser.add_argument('out_folder',
                    type=str,
                    action='store',
                    metavar='OUT_FOLDER',
                    help='Directory where the output file will be saved.')
parser.add_argument('--voxel_size',
                    type=float,
                    action='store',
                    metavar='VOXEL_SIZE',
                    help='Voxel size [m].')
parser.add_argument('--dynamic_viscosity',
                    type=float,
                    action='store',
                    metavar='DYNAMIC_VISCOSITY',
                    help='Dynamic viscosity [Pa.s].')
parser.add_argument('--temperature',
                    type=float,
                    action='store',
                    metavar='TEMPERATURE',
                    help='Temperature [K].')
parser.add_argument('--absolute_pressure',
                    type=float,
                    action='store',
                    metavar='ABSOLUTE_PRESSURE',
                    help='Absolute pressure [Pa].')
parser.add_argument('--pressure_gradient',
                    type=float,
                    action='store',
                    metavar='PRESSURE_GRADIENT',
                    help='Pressure gradient [Pa].')
arg = parser.parse_args()


def create_config_file(axis, xmax, ymax, zmax):
    config = {
        "setup": {
            "folder": arg.out_folder,
            "input_file": "centerlines.json",
            "shape": {
                "x": xmax,
                "y": ymax,
                "z": zmax,
            },
            "voxel_size": arg.voxel_size,
        },
        "simulation": {
            "fluid": [{
                "name": "water",
                "viscosity_behaviour": "constant",
                "properties": {
                    "dynamic_viscosity": arg.dynamic_viscosity
                }
            }],
            "algorithm": {
                "name": "static",
                "model": "poiseuille"
            },
            "experiment": {
                "flow_axis": axis,
                "temperature": arg.temperature,
                "absolute_pressure": arg.absolute_pressure,
                "boundary_thickness": 1,
                "boundary_condition": {
                    "driving_force": "pressure_gradient",
                    "value": arg.pressure_gradient
                }
            }
        }
    }

    axis_ref = {0: 'x', 1: 'y', 2: 'z'}

    # Write JSON file to disk
    with open(f'config_{axis_ref[axis]}.json', mode='w') as f:
        json.dump(config, f, indent=2)


def main():
    # Reading centerlines.json
    with open('centerlines.json', mode='r', encoding='utf-8') as file1:
        data = json.load(file1)

    # Extract node geometry arrays from JSON of rock sample centerlines
    nodes = sorted(data['graph']['nodes'], key=lambda node: int(node['id']))
    x = np.array([node['metadata']['node_coordinates']['x'] for node in nodes], dtype=np.double)
    y = np.array([node['metadata']['node_coordinates']['y'] for node in nodes], dtype=np.double)
    z = np.array([node['metadata']['node_coordinates']['z'] for node in nodes], dtype=np.double)

    xmax = int(np.amax(x))+1
    ymax = int(np.amax(y))+1
    zmax = int(np.amax(z))+1

    for ax in range(3):
        create_config_file(ax, xmax, ymax, zmax)


if __name__ == '__main__':
    main()
