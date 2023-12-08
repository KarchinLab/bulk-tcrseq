#!/usr/bin/env nextflow
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    btc/bulktcrseq
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Github : https://github.com/KarchinLab/bulk-tcrseq
----------------------------------------------------------------------------------------
*/

nextflow.enable.dsl = 2

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    VALIDATE & PRINT PARAMETER SUMMARY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

// Validate pipeline parameters
def checkPathParamList = [ params.sample_table, params.patient_table ]
for (param in checkPathParamList) { if (param) { file(param, checkIfExists: true) } }

// Check mandatory parameters
if (params.sample_table) { sample_table = file(params.sample_table) } else { exit 1, 'Sample table not specified. Please, provide a --sample_table=/path/to/sample_table.csv !' }
if (params.patient_table) { patient_table = file(params.patient_table) } else { exit 1, 'Patient table not specified. Please, provide a --patient_table=/path/to/patient_table.csv !' }
if (params.output_dir) { output_dir = params.output_dir } else { exit 1, 'Output directory not specified. Please, provide a --output_dir=/path/to/output_dir !' }

log.info """\
BTC - BULK TCRSEQ PIPELINE
===================================
Project parameters:
- Project Name              : ${params.project_name}
- Sample Table (CSV)        : ${params.sample_table}
- Patient Meta-data (CSV)   : ${params.patient_table}
- Output Directory          : ${params.output_dir}
"""

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT LOCAL MODULES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { CHECK_INPUT } from '../modules/local/check_input.nf'
include { CALC_SIMPLE } from '../modules/local/calc_simple.nf'
include { PLOT_SIMPLE } from '../modules/local/plot_simple.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

workflow BULKTCR {

    println("Welcome to the BULK TCRSEQ pipeline!")

    /////// =================== CHECK INPUT ===================  ///////
    CHECK_INPUT(
        file(params.sample_table), 
        file(params.patient_table) 
        )

    CHECK_INPUT.out.sample_utf8
        .splitCsv(header: true, sep: ',')
        .map { row -> 
            meta_map = [row.sample_id, row.patient_id, row.timepoint, row.origin] 
            [meta_map, file(row.file_path)]}
        .set { sample_map }

    /////// =================== CALC SIMPLE ===================  ///////
    CALC_SIMPLE( sample_map )

    CALC_SIMPLE.out.simple_csv
        .collectFile(name: 'combined_simple.csv', sort: true, 
                     storeDir: params.output_dir)
        .set { simple_stats_csv }
    
    CALC_SIMPLE.out.gene_usage_pkl
        .collect()
        .set { gene_usage_pkl }

    CALC_SIMPLE.out.sample_meta
        // .view()
        .collectFile(name: 'sample_meta.csv', sort: true)
        .set { sample_meta_csv }
    
    /////// =================== PLOT SIMPLE ===================  ///////
    PLOT_SIMPLE(
        file(params.sample_table),
        simple_stats_csv,
        gene_usage_pkl
        )
    
}