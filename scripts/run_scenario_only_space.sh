#! /bin/bash

source config.sh

export INPUT_DIR="$filespath/space"
export OUTPUT_DIR=/tmp

python $pyprojectpath/actuation/scenarios/only_space.py -i $INPUT_DIR -o $OUTPUT_DIR -c false