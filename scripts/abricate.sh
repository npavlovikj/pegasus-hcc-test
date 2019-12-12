#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load abricate

export PERL5LIB=/util/opt/anaconda/deployed-conda-envs/packages/abricate/envs/abricate-0.8.13/lib/5.26.2/:/util/opt/anaconda/deployed-conda-envs/packages/abricate/envs/abricate-0.8.13/lib/site_perl/5.26.2/:$PERL5LIB

abricate "$@"
