import vcfcli
import vcfcli.tools.parse_args
import vcfcli.onkopus_clients


def main():
    infile, outfile, genome_version, itype, otype, error_logfile, module = vcfcli.tools.parse_args.parse_args()

    if module == "uta":
        client = vcfcli.onkopus_clients.UTAAdapterClient(genome_version)
    vcfcli.process(infile, outfile, client)

if __name__ == "__main__":
    main()
