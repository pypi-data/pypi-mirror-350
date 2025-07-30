import unittest
from typing import List
import tracemalloc
import linecache
import gzip
import os
import pandas as pd
#from snpfilter import variant_filter

class TestVariantFilter(unittest.TestCase):

    def display_top(snapshot, key_type='lineno', limit=3):
        snapshot = snapshot.filter_traces((
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        ))
        top_stats = snapshot.statistics(key_type)

        print("Top %s lines" % limit)
        for index, stat in enumerate(top_stats[:limit], 1):
            frame = stat.traceback[0]
            # replace "/path/to/module/file.py" with "module/file.py"
            filename = os.sep.join(frame.filename.split(os.sep)[-2:])
            print("#%s: %s:%s: %.1f KiB"
                  % (index, filename, frame.lineno, stat.size / 1024))
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                print('    %s' % line)

        other = top_stats[limit:]
        if other:
            size = sum(stat.size for stat in other)
            print("%s other: %.1f KiB" % (len(other), size / 1024))
        total = sum(stat.size for stat in top_stats)
        print("Total allocated size: %.1f KiB" % (total / 1024))

    def test_variant_filter_dbsnp(self):
        """
        Test the variant filtering based on dbSNP frequency data

        :return:
        """

        vcf_data = pd.DataFrame({ 'chr':['chr9', 'chr14', 'chr5'],
                                  'pos':['35075025', '104773487', '180603376'],
                                  'id':['.','.','.'],
                                  'ref':['C', 'A', 'C'],
                                  'alt':['T', 'C', 'G'],
                                  'qual':["","",""],
                                  'filter':["","",""],
                                  'info':["","",""],
                                  'format':["","",""],
                                  'add':["","",""],
                                  'total':["0.0098","","0.00249"] }
                                , columns=['chr', 'pos', 'id', 'ref', 'alt', 'qual', 'filter', 'info', 'format','add', 'total'])
        vcf_data = vcf_data.astype("str")
        #vcf_data = variant_filter.filter_variants_dbsnp(vcf_data,threshold=0.004)
        vcf_data = vcf_data.reset_index(drop=True)

        vcf_ref = pd.DataFrame({ 'chr':['chr14', 'chr5'],
                                  'pos':['104773487', '180603376'],
                                  'id':['.','.'],
                                  'ref':['A', 'C'],
                                  'alt':['C', 'G'],
                                  'qual':["",""],
                                  'filter':["",""],
                                  'info':["",""],
                                  'format':["",""],
                                  'add':["",""],
                                  'total':["","0.00249"] }
                                , columns=['chr', 'pos', 'id', 'ref', 'alt', 'qual', 'filter', 'info', 'format','add', 'total'])

        vcf_ref = vcf_ref.astype("str")
        #pd.testing.assert_frame_equal(vcf_data, vcf_ref)

    def test_variant_filter_clinvar(self):
        """
        Test the variant filtering based on dbSNP frequency data

        :return:
        """

        vcf_data = pd.DataFrame({'chr': ['chr9', 'chr14', 'chr5','chr17'],
                                     'pos': ['35075025', '104773487', '180603376', '7673776'],
                                     'id': ['.', '.', '.','.'],
                                     'ref': ['C', 'A', 'C','G'],
                                     'alt': ['T', 'C', 'G','A'],
                                     'qual': ["", "", "",""],
                                     'filter': ["", "", "",""],
                                     'info': ["", "", "",""],
                                     'format': ["", "", "",""],
                                     'add': ["", "", "",""],
                                     'total': ["0.0098", "", "0.00249",""],
                                    'ClinicalSignificance': ['0','0','0','Pathogenic/Likely_pathogenic']
                                 }
                                    , columns=['chr', 'pos', 'id', 'ref', 'alt', 'qual', 'filter', 'info', 'format',
                                               'add', 'total', 'ClinicalSignificance'])
        vcf_data = vcf_data.astype("str")
        #vcf_data = variant_filter.filter_variants_clinvar(vcf_data, values=['Pathogenic/Likely_pathogenic'])
        vcf_data = vcf_data.reset_index(drop=True)

        vcf_ref = pd.DataFrame({'chr': ['chr9', 'chr14', 'chr5'],
                                    'pos': ['35075025','104773487', '180603376' ],
                                    'id': ['.', '.', '.'],
                                    'ref': ['C','A', 'C'],
                                    'alt': ['T', 'C', 'G'],
                                    'qual': ["", "",""],
                                    'filter': ["", "",""],
                                    'info': ["", "",""],
                                    'format': ["", "",""],
                                    'add': ["", "",""],
                                    'total': ["0.0098", '',"0.00249"],
                                    'ClinicalSignificance': ["0","0","0"]
                                }
                                   ,
                                   columns=['chr', 'pos', 'id', 'ref', 'alt', 'qual', 'filter', 'info', 'format', 'add',
                                            'total','ClinicalSignificance'])

        vcf_ref = vcf_ref.astype("str")
        #pd.testing.assert_frame_equal(vcf_data, vcf_ref)
