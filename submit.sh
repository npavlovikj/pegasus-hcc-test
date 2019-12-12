#!/bin/bash

set -e

export PYTHONPATH=`pegasus-config --python`

TOPDIR=`pwd`


# build a replica catalog, using the data we already transferred
echo "Finding existing data under /work/deogun/npavlovikj/FFH/pegasus-streptococcus-uberis-hcc/input_data ..."
rm -f rc-generated.txt
cp rc-base.txt rc-generated.txt
for ENTRY in `find /work/deogun/npavlovikj/FFH/pegasus-hcc-test/input_data -name \*.fastq`; do
    LFN=`basename $ENTRY`
    PFN=`echo "$ENTRY"`
    echo "$LFN  $PFN  site=\"local\"" >>rc-generated.txt
done

# Comment out for root-dax.py
export RUN_DIR=$TOPDIR/data_tmp
mkdir -p $RUN_DIR
./root-dax.py $RUN_DIR > root-pipeline.dax


# Comment out for sub-dax.py
# export RUN_DIR=$TOPDIR/data_tmp
# ./sub-dax.py $RUN_DIR > sub-pipeline.dax

# create the site catalog
cat > sites.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<sitecatalog xmlns="http://pegasus.isi.edu/schema/sitecatalog" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pegasus.isi.edu/schema/sitecatalog http://pegasus.isi.edu/schema/sc-4.0.xsd" version="4.0">

    <site  handle="local-hcc" arch="x86_64" os="LINUX">
        <directory type="shared-scratch" path="${PWD}/scratch">
            <file-server operation="all" url="file://${PWD}/scratch"/>
        </directory>
        <directory type="local-storage" path="${PWD}/outputs">
            <file-server operation="all" url="file://${PWD}/outputs"/>
        </directory>

        <profile namespace="pegasus" key="style">glite</profile>
        <!-- tell pegasus that local-hcc is accessible on submit host -->
        <profile namespace="pegasus" key="auxillary.local">true</profile>

        <profile namespace="condor" key="grid_resource">batch slurm</profile>
        <profile namespace="pegasus" key="queue">batch,tmp_anvil</profile>
        <profile namespace="env" key="PEGASUS_HOME">/usr</profile>
        <profile namespace="condor" key="request_memory"> ifthenelse(isundefined(DAGNodeRetry) || DAGNodeRetry == 0, 2000, 60000) </profile>
    </site>

</sitecatalog>
EOF


# plan and submit the root workflow
pegasus-plan --conf pegasusrc --sites local,local-hcc --output-site local-hcc --dir ${PWD} --dax root-pipeline.dax --submit # --cluster label


# plan and submit the sub workflow
# pegasus-plan --conf pegasusrc --sites local-hcc --output-site local-hcc --dir ${PWD} --dax sub-pipeline.dax --cluster label --submit


# to resume/restart fixed workflow
# pegasus-run /work/deogun/npavlovikj/FFH/pegasus-salmonella-test-array/npavlovikj/pegasus/pipeline/20190623T231524-0500
