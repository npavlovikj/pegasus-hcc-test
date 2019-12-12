#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load roary/3.12

export PERL5LIB=/util/opt/anaconda/deployed-conda-envs/packages/roary/envs/roary-3.12.0/lib/5.26.2/:/util/opt/anaconda/deployed-conda-envs/packages/roary/envs/roary-3.12.0/lib/site_perl/5.26.2/:$PERL5LIB

roary "$@"
# roary -e --mafft -p 12 -cd 100.0 *.gff -f $DATAOUT_DIRECTORY
tar -czvf roary_output.tar.gz roary_output
