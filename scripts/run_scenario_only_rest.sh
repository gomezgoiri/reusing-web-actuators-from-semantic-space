#! /bin/bash

source config.sh

export INPUT_DIR="$filespath/rest"
export OUTPUT_DIR=/tmp

python $pyprojectpath/actuation/scenarios/only_rest.py -i $INPUT_DIR -o $OUTPUT_DIR -e $eyebin -c false -n 10000