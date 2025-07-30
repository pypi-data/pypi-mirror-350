import unittest
import vcfcli


class AggregationTestCase(unittest.TestCase):

    def test_aggregator_client(self):
        genome_version = 'hg38'

        data = {"chr7:140753336A>T": {}, "chr12:25245350C>T": {}}
        variant_dc = {"0": "chr7:140753336A>T", "1": "chr12:25245350C>T"}

        variant_data = vcfcli.onkopus_clients.uta_adapter_client.UTAAdapterClient(
            genome_version=genome_version).process_vcf_chunk(data, variant_dc, None, input_format='json')
        print("uta response", variant_data)

        client = vcfcli.onkopus_clients.MetaKBClient(genome_version=genome_version)
        variant_data = client.process_vcf_chunk(variant_data, variant_dc, None, input_format='json')
        client = vcfcli.onkopus_clients.CIViCClient(genome_version=genome_version)
        variant_data = client.process_vcf_chunk(variant_data, variant_dc, None, input_format='json')
        client = vcfcli.onkopus_clients.OncoKBClient(genome_version=genome_version)
        variant_data = client.process_vcf_chunk(variant_data, variant_dc, None, input_format='json')

        # Aggregator
        variant_dc = vcfcli.generate_variant_dictionary(variant_data)
        variant_data = vcfcli.onkopus_clients.aggregator_client.ModuleClient(
            genome_version=genome_version).process_vcf_chunk(variant_data, variant_dc, None, input_format='json')

        print("Aggregator response ",variant_data)
