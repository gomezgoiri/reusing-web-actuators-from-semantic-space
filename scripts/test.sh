#! /bin/bash

source config.sh

export lamppth="$filespath/lamp"
export samplespth="$lamppth/samples"

$eyebin "$lamppth/lamp_ret.n3" "$lamppth/light_descpost.n3" "$lamppth/measure_descget.n3" "$lamppth/additional_info.n3" "$samplespth/light.n3" "$samplespth/tmpJ5_D3A.n3" --query "$lamppth/light_goal.n3"