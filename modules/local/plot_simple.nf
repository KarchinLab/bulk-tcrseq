// process to plot simple clonality measures from CLONALITY_CALC
process PLOT_SIMPLE {
    tag "${combined_clonality_csv}"
    label 'plot_simple'

    container "domebraccia/bulktcr:0.2"

    publishDir "${params.output_dir}/plot_simple", mode: 'copy'
    
    input:
    file combined_clonality_csv

    output:
    path 'clonality.png'
    path 'timecourse.png'
    path 'simple_stats.html'

    script:    
    """
    ## plot simple stats calculated from TCR counts data
    python $projectDir/bin/plot_simple.py \
        $combined_clonality_csv

    ## copy jupyter notebook to output directory
    cp $projectDir/notebooks/plot_simple.ipynb simple_stats.ipynb

    ## render ipynb report to html
    jupyter nbconvert simple_stats.ipynb --to html --execute
    """
    
    }
