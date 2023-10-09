process CLONALITY_CALC {
    tag "$clonality_calc"
    label 'process_single'

    //conda "conda-forge::python=3.8.3"
    debug true

    input:
    tuple val(sample_meta), path(count_table)

    // output:
    // *.html

    script:
    """
    echo "the sample metadata looks like: ${sample_meta}" 
    echo "the count table path is: ${count_table}" 
    #calc_clonality.py
    """

    stub:
    """
    echo "the sample metadata looks like: ${sample_meta}" 
    echo "accessing sample ID looks like: ${sample_meta[0]}"
    echo "accessing patient ID looks like: ${sample_meta[1]}"
    echo "accessing timepoint looks like: ${sample_meta[2]}"
    echo "accessing origin looks like: ${sample_meta[3]}"
    echo "the count table path is: ${count_table}" 
    """
}
