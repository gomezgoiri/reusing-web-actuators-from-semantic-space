#! /bin/bash

source config.sh

export INPUT_DIR="$filespath" # Under this directory, there must be at least two folders called "space" and "rest" with their files.
export OUTPUT_DIR=/tmp

python $pyprojectpath/actuation/eval/performance.py -i $INPUT_DIR -o $OUTPUT_DIR -e $eyebin  -c false -n 1