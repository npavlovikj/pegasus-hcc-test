#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load plasmidfinder

file=$1
output=$2

# plasmidfinder.py "$@"
mkdir $output
plasmidfinder.py -p $PLASMID_DB -i $file -o $output
# tar -czvf spades.tar.gz ./*_spades_output
tar -czvf ${output}.tar.gz ${output}
