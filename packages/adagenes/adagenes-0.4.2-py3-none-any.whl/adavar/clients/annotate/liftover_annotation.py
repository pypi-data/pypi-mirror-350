import traceback
import adagenes.conf.read_config as conf_reader
import time
from liftover import ChainFile
import adagenes


class LiftoverAnnotationClient:

    def __init__(self, genome_version=None, error_logfile=None):
        self.genome_version = genome_version
        self.data_dir = conf_reader.__LIFTOVER_DATA_DIR__

    def process_data(self, bframe, lo_hg19=None, lo_hg38=None, lo_t2t=None, target_genome=None) \
            -> adagenes.BiomarkerFrame:
        """

        :param bframe:
        :param lo_hg19:
        :param lo_hg38:
        :param lo_t2t:
        :param target_genome:
        :return:
        """

        start_time = time.time()
        adagenes.conf.check_liftover_files(conf_reader.__LIFTOVER_DATA_DIR__)

        isbframe = False
        if isinstance(bframe, adagenes.BiomarkerFrame):
            variant_data = bframe.data
            isbframe = True
        else:
            variant_data = bframe

        # Download liftover files if they cannot be found
        #adagenes.tools.check_liftover_files(conf_reader.__LIFTOVER_DATA_DIR__)

        vcf_lines_new = {}
        variant_count=0
        variants = {}

        #print(self.genome_version," target ",target_genome)

        if target_genome is None:
            if self.genome_version == "hg19":
                convert_go = "hg38"
                if lo_hg19 is None:
                    #print("load from liftover file (hg19)")
                    lo = ChainFile(conf_reader.__LIFTOVER_DATA_DIR__ + "/hg19ToHg38.over.chain.gz", one_based=True)
                    #lo = LiftOver(conf_reader.__LIFTOVER_DATA_DIR__ + "/hg19ToHg38.over.chain.gz")
                else:
                    lo = lo_hg19
            elif self.genome_version == "t2t":
                convert_go = "hg38"
                if lo_t2t is None:
                    lo = ChainFile(conf_reader.__LIFTOVER_DATA_DIR__ + "/hs1ToHg38.over.chain.gz",
                                          one_based=True)
                    #lo = LiftOver(conf_reader.__LIFTOVER_DATA_DIR__ + "/hs1ToHg38.over.chain.gz")
            else:
                convert_go = "hg19"
                liftover_file = conf_reader.__LIFTOVER_DATA_DIR__ + "/hg38ToHg19.over.chain.gz"
                #print(liftover_file)
                if lo_hg38 is None:
                    #print("load liftover from file (hg38)")

                    #adagenes.tools.liftover.check_liftover_files(conf_reader.__LIFTOVER_DATA_DIR__)
                    lo = ChainFile(liftover_file,
                                   one_based=True)
                    #lo = LiftOver(liftover_file)
                else:
                    lo = lo_hg38
        else:
            if target_genome == "hg19":
                convert_go = "hg19"

                if self.genome_version == "hg38":
                    liftover_file = conf_reader.__LIFTOVER_DATA_DIR__ + "/hg38ToHg19.over.chain.gz"
                elif self.genome_version == "t2t":
                    #liftover_file =
                    pass

                lo = ChainFile(liftover_file,
                               one_based=True)
                #lo = LiftOver(liftover_file)
            elif target_genome == "hg38":
                convert_go = "hg38"

                if self.genome_version == "hg19":
                    lo = ChainFile(conf_reader.__LIFTOVER_DATA_DIR__ + "/hg19ToHg38.over.chain.gz",
                                   one_based=True)
                    #lo = LiftOver(conf_reader.__LIFTOVER_DATA_DIR__ + "/hg19ToHg38.over.chain.gz")
                elif self.genome_version == "t2t":
                    lo = ChainFile(conf_reader.__LIFTOVER_DATA_DIR__ + "/hs1ToHg38.over.chain.gz",
                                   one_based=True)
                    #lo = LiftOver(conf_reader.__LIFTOVER_DATA_DIR__ + "/hs1ToHg38.over.chain.gz")
            elif target_genome == "t2t":
                convert_go = "t2t"
                if self.genome_version == "hg38":
                    #print("HG38 to T2T")
                    lo = ChainFile(conf_reader.__LIFTOVER_DATA_DIR__ + "/hg38ToGCA_009914755.4.over.chain.gz",
                                   one_based=True)
                    #lo = LiftOver(conf_reader.__LIFTOVER_DATA_DIR__ + "/hg38ToGCA_009914755.4.over.chain.gz")
                #elif self.genome_version == "hg19"
                #

        pos_key = "POS_" + self.genome_version
        #lo = LiftOver('hg19', 'hg38')
        if lo is None:
            return variant_data

        for var in variant_data.keys():

            if "variant_data" not in variant_data[var]:
                variant_data[var]["variant_data"] = {}

            if "POS" not in variant_data[var]["variant_data"]:
                chr, ref_seq, pos, ref, alt = adagenes.tools.parse_genomic_data.parse_genome_position(var)
                variant_data[var]["variant_data"]["CHROM"] = chr
                variant_data[var]["variant_data"]["POS"] = pos
                variant_data[var]["variant_data"]["POS_"+self.genome_version] = pos
                variant_data[var]["variant_data"]["REF"] = ref
                variant_data[var]["variant_data"]["ALT"] = alt

            chrom = 'chr' + str(variant_data[var]["variant_data"]["CHROM"])
            if pos_key in variant_data[var]["variant_data"]:
                pos = variant_data[var]["variant_data"][pos_key]
            else:
                variant_data[var]["variant_data"][pos_key] = variant_data[var]["variant_data"]["POS"]
                pos = variant_data[var]["variant_data"]["POS"]
            try:
                #print("get liftover: ",chrom,":",pos)
                #loc = lo.convert_coordinate(chrom, int(pos))
                loc = lo[chrom][int(pos)]
                #print("liftover position: ",loc)
                #print(type(loc))
                if len(loc)>0:
                    variant_data[var]["variant_data"]["POS_"+convert_go] = loc[0][1]
                    variant_data[var]["variant_data"]["strand"] = loc[0][2]
            except:
                print("Liftover error: Could not retrieve liftover position of ",var,": ",traceback.format_exc())

        stop_time = time.time() - start_time
        print("Liftover request: (", self.genome_version," to " , convert_go,")",stop_time)

        if isbframe:
            bframe.data = variant_data
            return bframe
        else:
            return variant_data

