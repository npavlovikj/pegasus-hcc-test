#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load snp-sites

file=$1
output=$2

snp-sites $file -m -p -o $output
# tar -czvf spades.tar.gz ./*_spades_output
tar -czvf ${output}.tar.gz ${output}*
