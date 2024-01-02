process CALC_SIMPLE {
    tag "${sample_meta[1]}"
    label 'process_single'

    container "domebraccia/bulktcr:0.3"

    publishDir "${params.output_dir}/simple_calc", mode: 'copy'

    input:
    tuple val(sample_meta), path(count_table)

    output:
    path 'simple_stats.csv', emit: simple_csv
    path 'v_family.csv', emit: v_family_csv
    path 'd_family.csv', emit: d_family_csv
    path 'j_family.csv', emit: j_family_csv
    val sample_meta        , emit: sample_meta

    script:
    """
    python $projectDir/bin/calc_simple.py \
        -m '${sample_meta}' \
        -c ${count_table} 
    """

    stub:
    """
    touch simple_calc.csv
    touch v_family.csv
    touch d_family.csv
    touch j_family.csv
    """
}
