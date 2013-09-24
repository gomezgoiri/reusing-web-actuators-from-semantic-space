#! /bin/bash

source config.sh

export INPUT_DIR=../files/lamp
export OUTPUT_DIR=/tmp

python $pyprojectpath/actuation/scenarios/only_rest.py -i $INPUT_DIR -o $OUTPUT_DIR -e $eulerjarpath -c false