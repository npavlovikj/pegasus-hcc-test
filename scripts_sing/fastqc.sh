#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load fastqc/0.11

fastqc "$@"
# fastqc pair_*_trimmed.fastq --extract
