from vcfcli.onkopus_clients import CCSGeneFusionClient
from vcfcli.tools import generate_keys


def fusion_request(gene_fusion_str: str, genome_version='hg38'):
    """
    Annotates gene fusions with associated Onkopus modules

    :param gene_fusion_str:
    :param genome_version:
    :return:
    """
    print("gene fusion query: ", gene_fusion_str)
    annotated_data = {}
    if gene_fusion_str != "":
        annotated_data[gene_fusion_str] = {}

        client = CCSGeneFusionClient(
            genome_version=genome_version)
        annotated_data = client.process_data(annotated_data)
        annotated_data = generate_keys(annotated_data)

    return annotated_data
