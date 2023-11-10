# Bulk TCR repertoire analysis

This repo contains the minimum viable pipeline for bulk TCR repertoire analysis.
The primary input are T cell clone counts from Bulk DNA TCR sequencing data from
Adaptive Biotechnologies. Future iterations of this pipeline will include 
options to process and analyze raw sequencing data from DNA and RNA TCRseq data. 

## Quick Start

We expect the user of this pipeline to be somewhat familiar with the command line and to have miniconda3 installed on 
their machine. If you do not have miniconda3 installed, please follow the instructions [here](https://docs.conda.io/en/latest/miniconda.html) 
to install it.

```
git clone https://github.com/KarchinLab/bulk-tcrseq.git
cd bulk-tcrseq
conda env create -f environment.yml
conda activate bulk-tcrseq
```

Once your environment is set up, run the pipeline with the following command:

```
nextflow run main.nf \
    --project_name=ribas_pd1 \
    --sample_table=assets/ribas_pd1_sample_table.csv \
    --patient_table=assets/ribas_pd1_patient_table.csv \
    --output_dir=outdir
```