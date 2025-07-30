import vcfcli

infile="/home/nadine/workspace/phd/data/patho_data/mtbreport_data/SNV_Genes_Variants_T_Cell.xlsx.annotated"
outfile = infile + ".tsv"

# export json file as tsv
bf = vcfcli.JSONReader().read_file(infile)
vcfcli.write_file(outfile, bf, file_type="tsv")

