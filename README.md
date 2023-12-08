# Bulk TCR repertoire analysis

This repo contains the minimum viable pipeline for bulk TCR repertoire analysis.
The primary input are T cell clone counts from Bulk DNA TCR sequencing data from
Adaptive Biotechnologies. Future iterations of this pipeline will include 
options to process and analyze raw sequencing data from DNA and RNA TCRseq data. 

## Requirements

### Nextflow

This pipeline is written in Nextflow, a workflow management system. To install Nextflow, follow the instructions [here](https://www.nextflow.io/docs/latest/getstarted.html#installation).

### Docker

This pipeline uses Docker containers to run the analysis. To install Docker, follow the instructions [here](https://docs.docker.com/get-docker/).

## Running the pipeline

```
nextflow run main.nf \
    --project_name=ribas_pd1 \
    --sample_table=assets/ribas_pd1_sample_table.csv \
    --patient_table=assets/ribas_pd1_patient_table.csv \
    --output_dir=<outdir>
```