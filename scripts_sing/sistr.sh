#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load sistr_cmd/1.0

sistr "$@"
