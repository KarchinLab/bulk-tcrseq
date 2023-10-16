process CLONALITY_CALC {
    tag "${sample_meta[1]}"
    label 'process_single'

    debug true 

    input:
    tuple val(sample_meta), path(count_table)

    output:
    path 'clonality.csv', emit: clonality_csv

    script:
    """
    python $projectDir/bin/calc_clonality.py \
        -m '${sample_meta}' \
        -c ${count_table} 
    """

    stub:
    """
    touch clonality.csv
    """
}
