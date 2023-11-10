// process to plot simple clonality measures from CLONALITY_CALC
process PLOT_SIMPLE {
    tag "${combined_clonality_csv}"
    label 'plot_simple'

    // container

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

    ## alternate way to render ipynb report to html with cmd line args
    #python $projectDir/bin/nb_wrapper.py simple_stats.ipynb --int_param 12

    ## render ipynb report to html
    jupyter nbconvert simple_stats.ipynb --to html --execute
    """
    
    }
