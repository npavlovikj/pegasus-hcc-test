#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load gubbins

file=$1
output=$2

run_gubbins.py -t fasttree -i 100 -m 3 -v $file -p $output
# tar -czvf spades.tar.gz ./*_spades_output
tar -czvf ${output}.tar.gz ${output}*
