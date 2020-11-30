#!/bin/bash

if (($# < 1));
    then echo -e "You need to specify the input file\n> ./downscale.sh <path>" && exit 1
fi

filepath="$1"

ffmpeg -i "$filepath" -vf  scale="352x240" output.mp4 && echo "successfully downscaled $filepath to "
