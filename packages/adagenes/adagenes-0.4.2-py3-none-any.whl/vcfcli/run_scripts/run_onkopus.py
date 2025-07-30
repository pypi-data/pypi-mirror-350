import vcfcli.onkopus_clients.uta_adapter_client as client
from vcfcli.tools import generate_variant_dictionary
from vcfcli import process_files
import vcfcli.tools.parse_args

description = """
========================================================================================================
  %%%%%%   %    %  %   %   %%%%%%   %%%%%%   %     %   %%%%%%  
 %      %  %%   %  %  %   %      %  %     %  %     %   %
 %      %  % %  %  %%%    %      %  %%%%%%   %     %   %%%%%%
 %      %  %  % %  %  %   %      %  %        %     %        %
  %%%%%%   %   %%  %   %   %%%%%%   %         %%%%%    %%%%%%   
========================================================================================================
"""

def main():
    infile, outfile, genome_version, itype, otype, error_logfile, module = vcfcli.tools.parse_args.parse_args()


    # Variant annotation
    # CCS
    obj = client.UTAAdapterClient(genome_version, error_logfile=error_logfile)
    processor = vcfcli.process_files.FileProcessor()
    biomarker_data = processor.process_file(infile, None, obj, genome_version=genome_version, input_format=itype,
                                            output_format=otype, output_type='obj', error_logfile=error_logfile)

    # dbSNP
    obj = vcfcli.vcf_clients.dbsnp_client.DBSNPClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # ClinVar
    obj = vcfcli.vcf_clients.clinvar_client.ClinVarClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # REVEL
    obj = vcfcli.vcf_clients.revel_client.REVELClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # LoFTool
    obj = vcfcli.vcf_clients.loftool_client.LoFToolClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # VUS-Predict
    obj = vcfcli.vcf_clients.vuspredict_client.VUSPredictClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # MVP
    obj = vcfcli.vcf_clients.mvp_client.MVPClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # CIViC
    obj = vcfcli.vcf_clients.civic_client.CIViCClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # OncoKB
    obj = vcfcli.vcf_clients.oncokb_client.ModuleClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    # MetaKB
    obj = vcfcli.vcf_clients.metakb_client.MetaKBClient(genome_version, error_logfile=error_logfile)
    variants = generate_variant_dictionary(biomarker_data)
    biomarker_data = obj.process_vcf_chunk(biomarker_data, variants, None, input_format='json')

    #print(biomarker_data)
    # Export biomarker data
    if otype == 'tsv':
        vcfcli.export_data(biomarker_data, outfile)
        outfile.close()

if __name__ == "__main__":
    main()
