process CALC_SIMPLE {
    tag "${sample_meta[1]}"
    label 'process_single'

    container "domebraccia/bulktcr:0.3"

    publishDir "${params.output_dir}/simple_calc", mode: 'copy'

    input:
    tuple val(sample_meta), path(count_table)

    output:
    path 'simple_stats.csv', emit: simple_csv
    path 'gene_usage_*.pkl', emit: gene_usage_pkl

    script:
    """
    python $projectDir/bin/calc_simple.py \
        -m '${sample_meta}' \
        -c ${count_table} 
    """

    stub:
    """
    touch simple_calc.csv
    """
}
