process CHECK_INPUT {
    tag "${sample_table}"

    container "domebraccia/bulktcr:0.1"

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
