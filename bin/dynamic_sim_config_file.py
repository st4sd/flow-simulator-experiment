#!/usr/bin/env python3

# © Copyright IBM Corp. 2022 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import json
import shutil

import numpy as np

parser = argparse.ArgumentParser(description='Generates a config file for a dynamic simulation \
    from a centerlines file.')
parser.add_argument('--replica',
                    type=str,
                    action='store',
                    metavar='REPLICA',
                    help='Replica number')
parser.add_argument('--centerlines',
                    type=str,
                    action='store',
                    metavar='CENTERLINES',
                    help='Centerlines file path (centerlines.json)')
parser.add_argument('--voxel_size',
                    type=float,
                    action='store',
                    required=True,
                    metavar='VOXEL_SIZE',
                    help='Voxel size [m].')
parser.add_argument('--contact_angle',
                    type=float,
                    action='store',
                    required=True,
                    metavar='CONTACT_ANGLE',
                    help='Contact angle [degree].')
parser.add_argument('--linear_mk',
                    type=float,
                    action='store',
                    required=True,
                    metavar='LINEAR_MK',
                    help='Linear MK.')
parser.add_argument('--interfacial_tension',
                    type=float,
                    action='store',
                    required=True,
                    metavar='INTERFACIAL_TENSION',
                    help='Interfacial tension [Pa].')
parser.add_argument('--temperature',
                    type=float,
                    action='store',
                    required=True,
                    metavar='TEMPERATURE',
                    help='Temperature [K]')
parser.add_argument('--absolute_pressure',
                    type=float,
                    action='store',
                    required=True,
                    metavar='ABSOLUTE_PRESSURE',
                    help='Absolute pressure [Pa].')
parser.add_argument('--pressure_gradient',
                    type=float,
                    action='store',
                    required=True,
                    metavar='PRESSURE_GRADIENT',
                    help='Pressure gradient driving force [Pa/m].')
parser.add_argument('--dynamic_viscosity_water',
                    type=float,
                    action='store',
                    required=True,
                    metavar='DYNAMIC_VISCOSITY_WATER',
                    help='Dynamic Viscosity of water [Pa.s].')
parser.add_argument('--dynamic_viscosity_co2',
                    type=float,
                    action='store',
                    required=True,
                    metavar='DYNAMIC_VISCOSITY_CO2',
                    help='Dynamic viscosity of co2 [Pa.s].')
parser.add_argument('--initial_time',
                    type=float,
                    action='store',
                    required=False,
                    default=0.0,
                    metavar='INITIAL_TIME',
                    help='Initial time [s].')
parser.add_argument('--final_time',
                    type=float,
                    action='store',
                    required=True,
                    metavar='FINAL_TIME',
                    help='Final time [s].')
parser.add_argument('--time_step_size',
                    type=float,
                    action='store',
                    required=True,
                    metavar='TIME_STEP_SIZE',
                    help='Time step size [s].')
arg = parser.parse_args()


def create_config_file(axis, xmax, ymax, zmax):
    config = {
        "setup": {
            "folder": ".",
            "input_file": "centerlines.json",
            "shape": {
                "x": xmax,
                "y": ymax,
                "z": zmax,
            },
            "voxel_size": arg.voxel_size,
        },
        "simulation": {
            "wettability": {
                "name": "CO2/fluid2/rock",
                "properties": {
                    "contact_angle": arg.contact_angle,
                    "linear_mk": arg.linear_mk
                }
            },
            "interface": {
                "name": "Water/CO2",
                "properties": {
                    "interfacial_tension": arg.interfacial_tension
                }
            },
            "fluid": [
                {
                    "name": "water",
                    "viscosity_behaviour": "constant",
                    "properties": {
                        "dynamic_viscosity": arg.dynamic_viscosity_water
                    }
                },
                {
                    "name": "co2",
                    "viscosity_behaviour": "constant",
                    "properties": {
                        "dynamic_viscosity": arg.dynamic_viscosity_co2
                    }
                }
            ],
            "algorithm": {
                "name": "dynamic",
                "model": "linear_molecular_kinetics",
                "initial_time": arg.initial_time,
                "final_time": arg.final_time,
                "time_step_size": arg.time_step_size,
                "relative_tolerance": 1.0e-4,
                "absolute_link_tolerance": 1.0e-3,
                "absolute_node_tolerance": 1.0e-3,
                "resume": True
                },
            "experiment": {
                "flow_axis": axis,
                "temperature": arg.temperature,
                "absolute_pressure": arg.absolute_pressure,
                "boundary_thickness": 1,
                "boundary_condition": {
                    "driving_force": "pressure_gradient_closed",
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
    # Copying centerlines
    shutil.copyfile(f"{arg.centerlines}/centerlines_{(arg.replica).rjust(4, '0')}.json",
                    "centerlines.json")

    # Reading centerlines.json
    with open("centerlines.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

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
