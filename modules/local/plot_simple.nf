// process to plot simple clonality measures from CLONALITY_CALC
process PLOT_SIMPLE {
    tag "${simple_stats_csv}"
    label 'plot_simple'

    container "domebraccia/bulktcr:0.3"

    publishDir "${params.output_dir}/plot_simple", mode: 'copy'
    
    input:
    path simple_stats_csv
    path gene_usage_pkl

    output:
    path 'num_clones.png'
    path 'clonality.png'
    path 'simpson_index_corrected.png'
    path 'pct_prod.png'
    path 'cdr3_avg_len.png'
    path 'simple_stats.html'

    script:    
    """
    ## plot simple stats calculated from TCR counts data
    python $projectDir/bin/plot_simple.py \
        $simple_stats_csv \
        $gene_usage_pkl

    ## copy quarto notebook to output directory
    cp $projectDir/notebooks/plot_simple.qmd simple_stats.qmd

    ## render qmd report to html
    quarto render simple_stats.qmd
    """
    
    }
