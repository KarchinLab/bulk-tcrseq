// process to plot simple clonality measures from CLONALITY_CALC
process PLOT_SIMPLE {
    tag "${simple_stats_csv}"
    label 'plot_simple'

    container "domebraccia/bulktcr:0.5"

    publishDir "${params.output_dir}/plot_simple", mode: 'copy'
    
    input:
    path sample_table
    path simple_stats_csv
    path v_family_csv

    output:
    path 'num_clones.png'
    path 'clonality.png'
    path 'simpson_index_corrected.png'
    path 'pct_prod.png'
    path 'cdr3_avg_len.png'
    path 'v_family_usage.png'
    path 'simple_stats.html'

    script:    
    """
    ## TEST
    echo "sample_table looks like: ${sample_table}"

    ## plot simple stats calculated from TCR counts data
    python $projectDir/bin/plot_simple.py \
        $sample_table \
        $simple_stats_csv \
        $v_family_csv

    ## copy quarto notebook to output directory
    cp $projectDir/notebooks/plot_simple.qmd simple_stats.qmd

    ## TEST
    echo "Work directory: $task.workDir"

    ## render qmd report to html
    quarto render simple_stats.qmd \
        -P project_name:$params.project_name \
        -P workflow_cmd:'$workflow.commandLine' \
        -P project_dir:$projectDir \
        -P sample_table:$sample_table \
        -P simple_stats_csv:$simple_stats_csv \
        -P v_family_csv:$v_family_csv \
        --to html
    """

    stub:
    """
    echo "1"
    """
    
    }
