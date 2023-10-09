process INPUT_CHECK {
    tag "$samplesheet"

    conda "conda-forge::python=3.8.3"
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/python:3.8.3' :
        'biocontainers/python:3.8.3' }"

    publishDir "${params.output_dir}/input_check", mode: 'copy'

    input:
    path sample_table
    path patient_table

    output:
    path 'sample_table_utf8.csv'    , emit: sample_utf8
    path 'patient_table_utf8.csv'   , emit: patient_utf8
    path 'sample_check.txt'
    path 'patient_check.txt'

    script: 
    """
    #!/bin/bash
    
    iconv -t utf-8 $sample_table > sample_table_utf8.csv
    iconv -t utf-8 $patient_table > patient_table_utf8.csv

    csvstat sample_table_utf8.csv > sample_check.txt
    csvstat patient_table_utf8.csv > patient_check.txt
    """

    stub:
    """
    #!/bin/bash

    touch sample_check.txt
    touch patient_check.txt
    """
}
