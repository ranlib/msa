#!/usr/bin/env python
"""
read in fasta file
determine sequence id  via blast
multiple sequence alignment via mafft
"""
import sys
import argparse
import ssl
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline

ssl._create_default_https_context = ssl._create_unverified_context

def get_best_hit(result_handle):
    """
    loop over blast results
    get name of best hit
    """
    name_of_best_hit = ""
    min_evalue = 1000
    for blast_record in NCBIXML.parse(result_handle):
        if blast_record.alignments:
            for align in blast_record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < min_evalue:
                        min_value = hsp.expect
                        name_of_best_hit = align.title
    return(name_of_best_hit)


#
# input
#
parser = argparse.ArgumentParser(description="blast", prog="blast", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
# blast
parser.add_argument("-i", "--input", dest="input", type=str, help="Fasta file with sequences", required=True)
parser.add_argument("-o", "--output", dest="output", type=str, help="Blast results (default=%(default)s)", default="results.xml")
parser.add_argument("-s", "--service", dest="service", type=str, help="Type of blast program (default=%(default)s)", default="blastn")
parser.add_argument("-e", "--evalue", dest="evalue", type=float, help="Evalue (default=%(default)f)", default=1e-20)
parser.add_argument("-n", "--nhits", dest="nhits", type=int, help="Number of hits (default=%(default)i)", default=5)
parser.add_argument("-d", "--database", dest="database", type=str, help="Database (default=%(default)s)", default="nr")
parser.add_argument("-a", "--alignments", dest="alignments", type=int, help="Number of alignments (default=%(default)i)", default=5)
# mafft
parser.add_argument("-f", "--format", dest="format", type=str, choices=("fasta", "clustalout"), help="mafft alignment output format (default=%(default)s)", default="fasta")
parser.add_argument("-m", "--msa", dest="msa", type=str, help="mafft alignment (default=%(default)s)", default="mafft.out")
parser.add_argument("-r", "--report", dest="report", type=str, help="mafft report (default=%(default)s)", default="mafft.report")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

#
# process input fasta file
# blastn all sequences
# blastx on Sequence1
#
records = []
with open(args.input, encoding="ascii") as input_file:
    # loop over sequences in input fasta file and run blast
    for record in SeqIO.parse(input_file, "fasta"):
        records.append(record)

# blastx Sequence1
result = NCBIWWW.qblast("blastx", args.database, str(records[0].seq), expect=args.evalue, ncbi_gi=False, descriptions="1", alignments=args.alignments, hitlist_size=args.nhits)
records[0].id = get_best_hit(result)

# run blastn service,
# use NCBI
# on 2. and 3. sequence
for record in records[1:]:
    result = NCBIWWW.qblast(args.service, args.database, str(record.seq), expect=args.evalue, ncbi_gi=False, descriptions="1", alignments=args.alignments, hitlist_size=args.nhits)
    record.id = get_best_hit(result)
    
# store new fasta records in output file
with open(args.output, "w", encoding="ascii") as output_fasta_handle:
    SeqIO.write(records, output_fasta_handle, "fasta")

#
# multiple alignment
# write alignment file and report file
clustalout = bool(args.format == "clustalout")
mafft_cline = MafftCommandline(input=args.output, clustalout=clustalout)
stdout, stderr = mafft_cline()

with open(args.msa, "w", encoding="ascii") as alignment_file:
    alignment_file.write(stdout)

with open(args.report, "w", encoding="ascii") as report_file:
    report_file.write(stderr)
