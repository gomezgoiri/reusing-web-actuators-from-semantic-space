#! /bin/bash

source config.sh

export INPUT_DIR=$filespath
export OUTPUT_DIR=/tmp

python $pyprojectpath/actuation/scenarios/mixed_space_rest.py -i $INPUT_DIR -o $OUTPUT_DIR -e $eulerjarpath -c false