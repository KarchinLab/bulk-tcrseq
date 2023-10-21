// process to plot simple clonality measures from CLONALITY_CALC
process PLOT_SIMPLE {
    tag "${combined_clonality_csv}"
    label 'plot_simple'

    publishDir "${params.output_dir}/plot_simple", mode: 'copy'
    
    input:
    file combined_clonality_csv

    output:
    path '*.png'

    script:    
    """
    python $projectDir/bin/plot_simple.py \
        $combined_clonality_csv
    """
    
    }
