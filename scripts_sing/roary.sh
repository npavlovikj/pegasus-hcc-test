#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load roary/3.12

roary "$@"
# roary -e --mafft -p 12 -cd 100.0 *.gff -f $DATAOUT_DIRECTORY
tar -czvf roary_output.tar.gz roary_output
