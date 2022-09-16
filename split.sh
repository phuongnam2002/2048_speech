#!/bin/bash

declare file="$1"
declare segs="$2"
declare prefix=${file: 0: $((${#file} -4))}
echo $prefix

for ((i = 0; i < segs; i++)); do
  declare sta="00:$(printf %02d $i)"
  declare dur="00:01"
  declare out="${prefix}_$(printf %02d $(($i+1))).wav"
  sox $file $out --show-progress trim $sta $dur
done
