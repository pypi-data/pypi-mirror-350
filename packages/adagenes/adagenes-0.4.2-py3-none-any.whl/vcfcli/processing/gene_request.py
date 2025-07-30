import vcfcli.processing.annotate_variants


def gene_request(gene_names, genome_version=None):
    if len(gene_names)>0:
        annotated_data = {}

        for gene in gene_names:
            annotated_data = vcfcli.processing.annotate_variants.annotate_gene_request(annotated_data, gene, genome_version=genome_version)

        return annotated_data
    else:
        return {}
