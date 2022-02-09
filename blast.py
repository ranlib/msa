#!/usr/bin/env python
"""
blastn/x sequence data against nr or nt
"""
import sys
import argparse
import ssl
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

ssl._create_default_https_context = ssl._create_unverified_context

#
# input
#
parser = argparse.ArgumentParser(description="blast", prog="blast", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
parser.add_argument("-i", "--input", dest="input", type=str, help="Fasta file with sequences", required=True)
parser.add_argument("-o", "--output", dest="output", type=str, help="Blast results (default=%(default)s)", default="results.xml")
parser.add_argument("-s", "--service", dest="service", type=str, help="Type of blast program (default=%(default)s)", default="blastn")
parser.add_argument("-e", "--evalue", dest="evalue", type=float, help="Evalue (default=%(default)f)", default=1e-20)
parser.add_argument("-a", "--alignments", dest="alignments", type=int, help="Number of alignments (default=%(default)i)", default=5)
parser.add_argument("-n", "--nhits", dest="nhits", type=int, help="Number of hits (default=%(default)i)", default=5)
parser.add_argument("-d", "--database", dest="database", type=str, help="Database (default=%(default)s)", default="nr")
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

with open(args.input, encoding="ascii") as input_file:
    result_handle = NCBIWWW.qblast(args.service, args.database, input_file.read(), expect=args.evalue, alignments=args.alignments, hitlist_size=args.nhits)

#
# write blast result to file
#
with open(args.output, "w", encoding="ascii") as save_file:
    blast_results = result_handle.read()
    save_file.write(blast_results)

#
# parse blast results
#
with open(args.output, encoding="ascii") as output_file:
    for record in NCBIXML.parse(output_file):
        if record.alignments:
            print(f"\nquery: {record.query}")
            for align in record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < args.evalue:
                        print(f"match: {align.title}")
