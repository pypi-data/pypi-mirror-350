import unittest
import adagenes

class TestVariantTypeRecognition(unittest.TestCase):

    def test_type_recognition(self):
        genome_version = 'hg19'
        data = {"chr7:140753336A>T": {}, "chr12:25245350C>T": {}}
        infile = "../test_files/somaticMutations.l12.txt"

        bframe = adagenes.BiomarkerFrame(data=data, genome_version=genome_version)
        bframe = adagenes.recognize_biomarker_types(bframe)
        #data = adagenes.TXTReader(genome_version).read_file(infile)
        #data = adagenes.TypeRecognitionClient(genome_version).process_data(data.data)
        print(data)


