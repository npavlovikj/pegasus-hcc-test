#!/bin/bash

#$5 = ""


a=`awk -F"\t" '{print $14}' $1 | tail -n 1`
b=`awk -F"\t" '{print $17}' $1 | tail -n 1`

if [ $a == 0 ] || [ $a -ge 300 ] || [ $b -le 25000 ]
then
echo "ignore"
#exit 0
#cp $2 $3
else
# use
#cp $2 $3
cp $2 $3/$4_contigs.fasta
#$5 = $4
fi

#for x in SRR*_contigs.fasta
#do
#echo $x "file://"`pwd`/$x
#done
