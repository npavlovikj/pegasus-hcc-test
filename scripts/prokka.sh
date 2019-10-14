#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load prokka/1.13

prokka "$@"
# prokka --kingdom Bacteria --locustag $N --outdir $DATAOUT/$N --prefix $N  $F
