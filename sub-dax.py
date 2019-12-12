#!/usr/bin/python

'''
USAGE: # ./sub-dax.py $RUN_DIR > sub-pipeline.dax
'''

import sys
import os

# Import the Python DAX library
os.sys.path.insert(0, "/usr/lib64/pegasus/python")
from Pegasus.DAX3 import *

dax = ADAG("pipeline")
base_dir = os.getcwd()

run_dir = "/work/deogun/npavlovikj/FFH/pegasus-hcc-test/data_tmp"

prokka_run = []
plasmidfinder_run = []
list_of_gff_files = []
list_of_contig_files = []
list_of_filtererd_sra_ids = []


for file_name in os.listdir(run_dir):
    filee = File(file_name)
    filee.addPFN(PFN("file://{0}/".format(run_dir) + str(file_name), "local-hcc"))
    dax.addFile(filee)
    list_of_contig_files.append(filee)


i = 0
for output_filtering_contigs in list_of_contig_files:

    srr_id = output_filtering_contigs.name.split("_")[0]
		
    # add job for Prokka
    prokka_run.append(Job("ex_prokka_run"))
    prokka_run[i].addArguments("--kingdom", "Bacteria", "--locustag", srr_id, "--outdir", str(srr_id) + "_prokka_output", "--prefix", srr_id, "--force", output_filtering_contigs)
    prokka_run[i].uses(output_filtering_contigs, link=Link.INPUT)
    prokka_run[i].uses(str(srr_id) + "_prokka_output/" + str(srr_id) + ".gff", link=Link.OUTPUT, transfer=False)
    prokka_run[i].addProfile(Profile("pegasus", "label", str(srr_id)))
    dax.addJob(prokka_run[i])
    # add files
    f = File(str(srr_id) + "_prokka_output/" + str(srr_id) + ".gff")
    list_of_gff_files.append(f)


    # add job for plasmidfinder
    # only ... should be transferred
    # plasmidfinder.py -p $PLASMID_DB -i 00837_11_contigs.fa -o $DATAOUT
    # make tarball from directory
    plasmidfinder_run.append(Job("ex_plasmidfinder_run"))
#    plasmidfinder_run[i].addArguments("-p", "$PLASMID_DB", "-i", output_filtering_contigs, "-o", str(srr_id) + "_plasmidfinder_output")
    plasmidfinder_run[i].addArguments(output_filtering_contigs, str(srr_id) + "_plasmidfinder_output")
    plasmidfinder_run[i].uses(output_filtering_contigs, link=Link.INPUT)
    plasmidfinder_run[i].uses(str(srr_id) + "_plasmidfinder_output.tar.gz", link=Link.OUTPUT, transfer=True)
    plasmidfinder_run[i].addProfile(Profile("pegasus", "label", str(srr_id)))
    dax.addJob(plasmidfinder_run[i])

    i = i + 1


# add job for sistr
# only ... should be transferred
# sistr --qc -vv --alleles-output allele_results.json --novel-alleles novel_alleles.fasta --cgmlst-profiles cgmlst_profiles.csv -f csv -o sistr_output.csv *.fasta
#sistr_run = Job("ex_sistr_run")
#sistr_run.addArguments("--qc", "-vv", "--alleles-output", "allele_results.json", "--novel-alleles", "novel_alleles.fasta", "--cgmlst-profiles", "cgmlst_profiles.csv", "-f", "csv", "-o", "sistr_output.csv", *list_of_contig_files)
#for l in list_of_contig_files:
#    sistr_run.uses(l, link=Link.INPUT)
#sistr_run.uses("sistr_output.csv", link=Link.OUTPUT, transfer=True)
#sistr_run.addProfile(Profile("pegasus", "label", str(srr_id)))
#dax.addJob(sistr_run)

# add job for mlst
# only ... should be transferred
# mlst --legacy --scheme senterica *.fa --csv > salmonellast_output.csv
mlst_run = Job("ex_mlst_run")
mlst_run.addArguments("--legacy", "--scheme", "suberis", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    mlst_run.uses(l, link=Link.INPUT)
o = File("mlst_output.csv")
mlst_run.setStdout(o)
mlst_run.uses(o, link=Link.OUTPUT, transfer=True)
mlst_run.addProfile(Profile("pegasus", "runtime", "108000"))
mlst_run.addProfile(Profile("globus", "maxwalltime", "1800"))
#mlst_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(mlst_run)

# add job for abricate vfdb
# only ... should be transferred
# --db vfdb *.fa --csv
abricate_vfdb_run = Job("ex_abricate_run")
abricate_vfdb_run.addArguments("--db", "vfdb", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    abricate_vfdb_run.uses(l, link=Link.INPUT)
o = File("sabricate_vfdb_output.csv")
abricate_vfdb_run.setStdout(o)
abricate_vfdb_run.uses(o, link=Link.OUTPUT, transfer=True)
#abricate_vfdb_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(abricate_vfdb_run)

# add job for abricate argannot
# only ... should be transferred
# abricate --db argannot *.fa --csv
abricate_argannot_run = Job("ex_abricate_run")
abricate_argannot_run.addArguments("--db", "argannot", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    abricate_argannot_run.uses(l, link=Link.INPUT)
o = File("sabricate_argannot_output.csv")
abricate_argannot_run.setStdout(o)
abricate_argannot_run.uses(o, link=Link.OUTPUT, transfer=True)
#abricate_argannot_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(abricate_argannot_run)

# add job for abricate card
# only ... should be transferred
# abricate --db card *.fa --csv
abricate_card_run = Job("ex_abricate_run")
abricate_card_run.addArguments("--db", "card", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    abricate_card_run.uses(l, link=Link.INPUT)
o = File("sabricate_card_output.csv")
abricate_card_run.setStdout(o)
abricate_card_run.uses(o, link=Link.OUTPUT, transfer=True)
#abricate_card_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(abricate_card_run)

# add job for abricate ncbi
# only ... should be transferred
# abricate --db ncbi *.fa --csv
abricate_ncbi_run = Job("ex_abricate_run")
abricate_ncbi_run.addArguments("--db", "ncbi", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    abricate_ncbi_run.uses(l, link=Link.INPUT)
o = File("sabricate_ncbi_output.csv")
abricate_ncbi_run.setStdout(o)
abricate_ncbi_run.uses(o, link=Link.OUTPUT, transfer=True)
#abricate_ncbi_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(abricate_ncbi_run)

# add job for abricate plasmidfinder
# only ... should be transferred
# abricate --db plasmidfinder *.fa --csv
abricate_plasmidfinder_run = Job("ex_abricate_run")
abricate_plasmidfinder_run.addArguments("--db", "plasmidfinder", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    abricate_plasmidfinder_run.uses(l, link=Link.INPUT)
o = File("sabricate_plasmidfinder_output.csv")
abricate_plasmidfinder_run.setStdout(o)
abricate_plasmidfinder_run.uses(o, link=Link.OUTPUT, transfer=True)
#abricate_plasmidfinder_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(abricate_plasmidfinder_run)

# add job for abricate resfinder
# only ... should be transferred
# abricate --db resfinder *.fa --csv
abricate_resfinder_run = Job("ex_abricate_run")
abricate_resfinder_run.addArguments("--db", "resfinder", "--csv", *list_of_contig_files)
for l in list_of_contig_files:
    abricate_resfinder_run.uses(l, link=Link.INPUT)
o = File("sabricate_resfinder_output.csv")
abricate_resfinder_run.setStdout(o)
abricate_resfinder_run.uses(o, link=Link.OUTPUT, transfer=True)
#abricate_resfinder_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(abricate_resfinder_run)

# add job for Roary
roary_run = Job("ex_roary_run")
roary_run.addArguments("-s", "-e", "--mafft", "-p", "4", "-cd", "99.0", "-i", "95", "-f", "roary_output", *list_of_gff_files)
for l in list_of_gff_files:
    roary_run.uses(l, link=Link.INPUT)
roary_run.uses("roary_output/core_gene_alignment.aln", link=Link.OUTPUT, transfer=True)
roary_run.uses("roary_output.tar.gz", link=Link.OUTPUT, transfer=True)
roary_run.addProfile(Profile("pegasus", "runtime", "108000"))
roary_run.addProfile(Profile("globus", "maxwalltime", "1800"))
roary_run.addProfile(Profile("condor", "request_memory", "150000"))
roary_run.addProfile(Profile("globus", "maxmemory", "150000"))
roary_run.addProfile(Profile("pegasus", "memory", "150000"))
#roary_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(roary_run)

# add job for baps_run
# R script, wrapper
fastbaps_run = Job("ex_fastbaps_run")
fastbaps_output = File("fastbaps_baps.csv")
fastbaps_run.addArguments("roary_output/core_gene_alignment.aln", fastbaps_output)
fastbaps_run.uses("roary_output/core_gene_alignment.aln", link=Link.INPUT)
fastbaps_run.uses(fastbaps_output, link=Link.OUTPUT, transfer=True)
fastbaps_run.addProfile(Profile("condor", "request_memory", "30000"))
fastbaps_run.addProfile(Profile("globus", "maxmemory", "30000"))
fastbaps_run.addProfile(Profile("pegasus", "memory", "30000"))
#baps_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(fastbaps_run)

# ls
ls_run = Job("ex_ls")
ls_run.addArguments(run_dir)
#ls_run.addProfile(Profile("pegasus", "label", str(srr_id)))
dax.addJob(ls_run)

length = len(list_of_filtererd_sra_ids)
for i in range(0,length):
    # Add control-flow dependencies
    dax.addDependency(Dependency(parent=plasmidfinder_run[i], child=ls_run))
    dax.addDependency(Dependency(parent=quast_run[i], child=prokka_run[i]))
    dax.addDependency(Dependency(parent=prokka_run[i], child=roary_run))
dax.addDependency(Dependency(parent=mlst_run, child=ls_run))
dax.addDependency(Dependency(parent=abricate_argannot_run, child=ls_run))
dax.addDependency(Dependency(parent=abricate_card_run, child=ls_run))
dax.addDependency(Dependency(parent=abricate_ncbi_run, child=ls_run))
dax.addDependency(Dependency(parent=abricate_plasmidfinder_run, child=ls_run))
dax.addDependency(Dependency(parent=abricate_resfinder_run, child=ls_run))
dax.addDependency(Dependency(parent=abricate_vfdb_run, child=ls_run))
dax.addDependency(Dependency(parent=roary_run, child=fastbaps_run))


# Write the DAX to stdout
dax.writeXML(sys.stdout)
