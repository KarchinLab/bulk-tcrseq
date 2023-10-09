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
- Patient Meta-data (CSV)   : ${params.patient_meta}
- Output Directory          : ${params.output_dir}
"""

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    IMPORT LOCAL MODULES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { INPUT_CHECK } from './modules/local/input_check.nf'
include { CLONALITY_CALC } from './modules/local/clonality_calc.nf'

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN MAIN WORKFLOW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

workflow {

    println("Welcome to the BULK TCRSEQ pipeline!")

    println("-- Running input check...")
    INPUT_CHECK(
        file(params.sample_table), 
        file(params.patient_table)
        )
    
    // INPUT_CHECK.out.sample_utf8.view()
    // INPUT_CHECK.out.patient_utf8.view()

    // println("-- Running simple clonality clac...")
    INPUT_CHECK.out.sample_utf8
        .splitCsv(header: true, sep: ',')
        .map { row -> 
            meta_map = [row.sample_id, row.patient_id, row.timepoint, row.origin] 
            [meta_map, file(row.file_path)]}
        .set { sample_map }
        // .view()

    CLONALITY_CALC(
        sample_map
        )
}