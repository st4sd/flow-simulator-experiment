# Integrated Flow Experiments

## Run simulations using the Docker backend of ST4SD

### Prerequisites

1. A recent version of python 3 - [python 3.7+](https://www.python.org/downloads/)
2. The [docker](https://docs.docker.com/get-docker/) container runtime
3. The [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) command-line utility


### Instructions

You can try out the experiment on your laptop by:

1. creating a python virtual environment, activating it, and installing the python module `st4sd-runtime-core[deploy]`
2. cloning this repository
3. creating `simulations-data` folder to be used as an application dependency
4. launching the experiment

For example:

```bash
#!/usr/bin/env sh
# Download virtual experiment
git clone https://github.com/st4sd/flow-simulator-experiment.git
cd flow-simulator-experiment
# Setup ST4SD runtime-core
python3 -m venv --copies venv
. venv/bin/activate
python3 -m pip install "st4sd-runtime-core[deploy]"
# Run Experiment
cat <<EOF >variables.yaml
global:
  variable1: <variable1_value>
  variable2: <variable2_value>
  variable3: <variable3_value>
EOF
time elaunch.py --platform docker --dockerExecutableOverride=/path/to/my/docker/executable \
    -s simulations-data:/path/to/my/my-simulations-data/on/my-disk:copy \
    -a variables.yaml  --manifest path/to/your/manifest.yaml path/to/your/flowir_package.yaml
# See outputs of experiment
output_dir=$(ls -td flowir_package*.instance | head -1)
ls -lth ${output_dir}
cat "${output_dir}/output/output.json"
```

If `podman` is the docker executable being used, it is necessary to run
```bash
podman machine set --rootful
```
before running
```bash
podman machine start
```

## Running Simulations Coupled with the Geometry Modification Module

1. Fill the file `conf/flowir_package_gmm.yaml` with your input data.
1. Create a new folder inside `simulations-data` with a `centerlines.json` file and a CSV file listing the input cases. You may also add a `binary_image.raw` file, but it is optional. GMM will use the provided `centerlines.json` if the `binary_image.raw` is not found.
1. To create the `variables.yaml` file, run the following command replacing the values if needed:
```bash
cat <<EOF >variables.yaml
global:
  s3Folder: "my_simulation_folder"
  centerlinesFile: "centerlines"
  csvFile: "my_cases_file.csv"
  numberOfCases: 3
  binaryImage: "binary_image"
EOF
```
1. Run `elaunch.py` command replacing the path to your `simulations-data` folder. If you are using docker, the `--dockerExecutableOverride` flag is not necessary.
```bash
time elaunch.py --platform docker --dockerExecutableOverride=/path/to/my/docker/executable \
    -s simulations-data:/path/to/my/my-simulations-data/on/my-disk:copy \
    -a variables.yaml --manifest manifest.yaml conf/flowir_package_gmm.yaml
```

## Running Static Simulations

1. Fill the file `conf/flowir_package_static.yaml` with your input data.
1. Create a new folder inside `simulations-data` with a `rock-centerlines.json` file. 
1. To create the `variables.yaml` file, run the following command replacing the values if needed:
```bash
cat <<EOF >variables.yaml
global:
  numberOfNetworks: 30
  s3Folder: "my_simulation_folder"
  sampleFileName: "rock-centerlines.json"
  voxelSize_m: 2.25e-6
  capillaryLength_m: 4.5e-5
  sampleSize_m: 3.0e-4
  dynamicViscosity_Pas: 1.002e-3
  temperature_K: 340.0
  absolutePressure_Pa: 101325.0
  pressureGradient_Pa: 10132.5
EOF
```
1. Run `elaunch.py` command replacing the path to your `simulations-data` folder. If you are using docker, the `--dockerExecutableOverride` flag is not necessary.
```bash
time elaunch.py --platform docker --dockerExecutableOverride=/path/to/my/docker/executable \
    -s simulations-data:/path/to/my/my-simulations-data/on/my-disk:copy \
    -a variables.yaml --manifest manifest.yaml conf/flowir_package_static.yaml
```

## Running Dynamic Simulations

1. Fill the file `conf/flowir_package_dynamic.yaml` with your input data.
1. Create a new folder inside `simulations-data` with a `centerlines.tar` file (see instructions about this file below).
1. To create the `variables.yaml` file, run the following command replacing the values if needed:
```bash
cat <<EOF >variables.yaml
global:
  numberOfCenterlines: 30
  s3Folder: "my_simulation_folder"
  voxelSize_m: 2.25e-6
  capillaryLength_m: 4.5e-5
  sampleSize_m: 3.0e-4
  contactAngle_deg: 0.0
  linearMK: 0.0
  interfacialTension_Nm: 0.04
  temperature_K: 400.0
  absolutePressure_Pa: 10000000.0
  pressureGradient_Pa_m: 10e6
  dynamicViscosityWater_Pas: 0.000260196
  dynamicCiscosityCO2_Pas: 3.26e-5
  initialTime_s: 0.0
  finalTime_s: 0.05
  timeStepSize_s: 0.001
EOF
```
1. Run `elaunch.py` command replacing the path to your `simulations-data` folder. If you are using docker, the `--dockerExecutableOverride` flag is not necessary.
```bash
time elaunch.py --platform docker --dockerExecutableOverride=/path/to/my/docker/executable \
    -s simulations-data:/path/to/my/my-simulations-data/on/my-disk:copy \
    -a variables.yaml --manifest manifest.yaml conf/flowir_package_dynamic.yaml
```

## Centerlines files

To perform dynamic simulations it is required to provide the centerlines to be used. They should be all in a single compressed file named `centerlines.tar` and each centerline must follow the following name convenction:

- `centerlines`
    - `centerlines_0000.json`
    - `centerlines_0001.json`
    - `centerlines_0002.json`
    - `...`
