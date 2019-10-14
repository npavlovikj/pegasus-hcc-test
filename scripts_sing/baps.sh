#!/bin/bash

. /util/opt/lmod/lmod/init/profile
export -f module
module use /util/opt/hcc-modules/Common/

module load r-rhierbaps

file=$1
output=$2

cat > baps.R <<EOF
# Load library
library("rhierbaps")

# Set seed to reproduce results
set.seed(1234)

# Load data
# input_file <- system.file("extdata", "core_gene_alignment.fa", package = "rhierbaps")
input_file <- ape::read.dna("roary_output/core_gene_alignment.aln", format="fasta")
snp_matrix <- load_fasta(input_file)
hb_results <- hierBAPS(snp_matrix, max.depth = 1, n.pops = 150, n.extra.rounds = Inf, quiet = TRUE)
write.csv(hb_results\$partition.df, file = "hierbaps_partition.csv", col.names = TRUE, row.names = FALSE)
EOF

Rscript baps.R
