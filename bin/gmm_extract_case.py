#!/usr/bin/env python3

# © Copyright IBM Corp. 2023 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import ast
import json
import os

import pandas as pd

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generates JSON file from respective CSV replica line.')
parser.add_argument('out_folder',
                    type=str,
                    action='store',
                    metavar='OUT_FOLDER',
                    help='Directory containing output file.')
parser.add_argument('--replica',
                    type=str,
                    action='store',
                    metavar='REPLICA',
                    help='Replica number.')
parser.add_argument('--csv_file',
                    type=str,
                    action='store',
                    required=True,
                    metavar='CSV_FILE',
                    help='CSV input file.')
arg = parser.parse_args()

input_csv = pd.read_csv(arg.csv_file, engine="python", sep=None, header=0, encoding='utf-8')
input_csv = input_csv.fillna(0)
replica_line = int(arg.replica)

deposition_references = input_csv.iloc[replica_line]['deposition_references']
dissolution_references = input_csv.iloc[replica_line]['dissolution_references']
erosion_references = input_csv.iloc[replica_line]['erosion_references']
precipitation_references = input_csv.iloc[replica_line]['precipitation_references']
experiment_parameters_information = input_csv.iloc[replica_line]['experiment_parameters_information']

case_json = {
  "setup": {
    "experiment_name": str(input_csv.iloc[replica_line]['experiment_name']),
    "experiment_description": str(input_csv.iloc[replica_line]['experiment_description']),
    "time_steps": int(input_csv.iloc[replica_line]['time_steps']),
    "processes": {
      "deposition": bool(input_csv.iloc[replica_line]['deposition']),
      "dissolution": bool(input_csv.iloc[replica_line]['dissolution']),
      "erosion": bool(input_csv.iloc[replica_line]['erosion']),
      "precipitation": bool(input_csv.iloc[replica_line]['precipitation'])
    },
    "outputs": {
      "erosion": [
        "erosion_onset",
        "erosion_rate",
        "erosion_shear_stress",
        "erosion_time_scale"
      ],
      "flow": [
        "maximum_flow_rate",
        "maximum_reynolds_number",
        "pressure_gradients",
        "reynolds_number",
        "wall_shear_stress"
      ],
      "geometry": [
        "accumulated_volume_time_step",
        "aspect_ratio",
        "inlet_link_radius",
        "link_length",
        "link_radius",
        "pore_volume",
        "porosity",
        "porosity_time_step",
        "reactive_area",
        "total_accumulated_volume_simulation",
        "total_accumulated_volume_time_step",
        "void_space_volume",
        "void_space_volume_ratio"
      ],
      "precipitation": [
        "maximum_precipitation_rate",
        "precipitation_clogging_evolution",
        "precipitation_number_clogged_inlet_links",
        "precipitation_number_clogged_links"
      ],
      "static": [
        "flow_rate",
        "flow_speed",
        "permeability",
        "pressure"
      ]
    }
  },
  "simulation": {
    "flow": {
      "algorithm": {
        "name": "static",
        "model": "poiseuille"
      },
      "experiment": {
        "flow_axis": int(input_csv.iloc[replica_line]['flow_axis']),
        "temperature": float(input_csv.iloc[replica_line]['temperature']),
        "absolute_pressure": float(input_csv.iloc[replica_line]['absolute_pressure']),
        "boundary_thickness": int(input_csv.iloc[replica_line]['boundary_thickness']),
        "boundary_condition": {
          "driving_force": str(input_csv.iloc[replica_line]['driving_force']),
          "value": float(input_csv.iloc[replica_line]['value'])
        }
      }
    },
    "sample": {
      "sample_name": str(input_csv.iloc[replica_line]['sample_name']),
      "inlet_links_identification": {
        "pressure_threshold_method": str(input_csv.iloc[replica_line]['pressure_threshold_method'])
      },
      "parameters": {
        "initial_porosity": {
          "porosity_method": str(input_csv.iloc[replica_line]['porosity_method']),
        },
        "minimum_link_radius": float(input_csv.iloc[replica_line]['minimum_link_radius']),
        "sample_origin": ast.literal_eval(input_csv.iloc[replica_line]['sample_origin']),
        "sample_size": ast.literal_eval(input_csv.iloc[replica_line]['sample_size']),
        "voxel_size": float(input_csv.iloc[replica_line]['voxel_size'])
      }
    },
    "phases": {
      "liquid": {
        "liquid_name": str(input_csv.iloc[replica_line]['liquid_name']),
        "viscosity_behaviour": str(input_csv.iloc[replica_line]['viscosity_behaviour']),
        "properties": {
          "liquid_density": float(input_csv.iloc[replica_line]['liquid_density']),
          "liquid_dynamic_viscosity": float(input_csv.iloc[replica_line]['liquid_dynamic_viscosity'])
        }
      },
      "solid": {
        "solid_name": str(input_csv.iloc[replica_line]['solid_name']),
        "properties": {
          "solid_density": float(input_csv.iloc[replica_line]['solid_density']),
          "solid_molar_weight": float(input_csv.iloc[replica_line]['solid_molar_weight'])
        }
      }
    },
    "processes": {
      "deposition": {
        "model": {
          "name": "jager2017",
          "deposition_method": str(input_csv.iloc[replica_line]['deposition_method'])
        },
        "parameters": {
          "deposition_coefficient": float(input_csv.iloc[replica_line]['deposition_coefficient']),
          "deposition_reaction_time": float(input_csv.iloc[replica_line]['deposition_reaction_time']),
          "erosion_coefficient": float(input_csv.iloc[replica_line]['erosion_coefficient']),
          "relative_concentration": float(input_csv.iloc[replica_line]['relative_concentration'])
        },
        "deposition_references": ast.literal_eval(deposition_references) if deposition_references != 0 else []
      },
      "dissolution": {
        "model": {
          "name": "molins2021",
          "dissolution_rate_method": str(input_csv.iloc[replica_line]['dissolution_rate_method']),
        },
        "parameters": {
          "activity_coefficient": float(input_csv.iloc[replica_line]['activity_coefficient']),
          "dissolution_rate_constant": float(input_csv.iloc[replica_line]['dissolution_rate_constant']),
          "dissolution_reaction_time": float(input_csv.iloc[replica_line]['dissolution_reaction_time']),
          "inlet_concentration": float(input_csv.iloc[replica_line]['inlet_concentration']),
          "dissolution_parameters_information": str(input_csv.iloc[replica_line]['dissolution_parameters_information'])
        },
        "dissolution_references": ast.literal_eval(dissolution_references) if dissolution_references != 0 else []
      },
      "erosion": {
        "model": {
          "name": "jager2017",
          "erosion_method": str(input_csv.iloc[replica_line]['erosion_method'])
        },
        "parameters": {
          "erosion_coefficient": float(input_csv.iloc[replica_line]['erosion_coefficient']),
          "erosion_reaction_time": float(input_csv.iloc[replica_line]['erosion_reaction_time'])
        },
        "erosion_references": ast.literal_eval(erosion_references) if erosion_references != 0 else []
      },
      "precipitation": {
        "clogging": {
          "simulation_stop_criteria": str(input_csv.iloc[replica_line]['simulation_stop_criteria'])
        },
        "model": {
          "name": "noiriel2012",
          "precipitation_rate_method": str(input_csv.iloc[replica_line]['precipitation_rate_method']),
          "regression_method": str(input_csv.iloc[replica_line]['regression_method'])
        },
        "parameters": {
          "calcium_concentration_variation": float(input_csv.iloc[replica_line]['calcium_concentration_variation']),
          "experiment_factor": float(input_csv.iloc[replica_line]['experiment_factor']),
          "m_coefficient": float(input_csv.iloc[replica_line]['m_coefficient']),
          "n_coefficient": float(input_csv.iloc[replica_line]['n_coefficient']),
          "precipitation_rate": float(input_csv.iloc[replica_line]['precipitation_rate']),
          "precipitation_rate_constant": float(input_csv.iloc[replica_line]['precipitation_rate_constant']),
          "precipitation_reaction_time": float(input_csv.iloc[replica_line]['precipitation_reaction_time']),
          "saturation_index": float(input_csv.iloc[replica_line]['saturation_index']),
          "experiment_parameters_information": ast.literal_eval(experiment_parameters_information) if experiment_parameters_information != 0 else []
        },
        "precipitation_references": ast.literal_eval(precipitation_references) if precipitation_references != 0 else []
      }
    }
  }
}

with open(os.path.join(arg.out_folder, 'case_input.json'), mode='w') as case_file:
    json.dump(case_json, case_file, indent=2)
