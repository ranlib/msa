#!/usr/bin/env python
"""
run mafft
"""
import sys
import argparse
from Bio.Align.Applications import MafftCommandline

parser = argparse.ArgumentParser(description="mafft", prog="mafft", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
parser.add_argument("-i", "--input", dest="input", type=str, help="fasta file with sequences", required=True)
parser.add_argument("-o", "--output", dest="output", type=str, help="mafft alignment (default=%(default)s)", default="mafft.out")
parser.add_argument("-e", "--error", dest="error", type=str, help="mafft report (default=%(default)s)", default="mafft.err")
parser.add_argument("-f", "--format", dest="format", type=str, choices=("fasta", "clustalout"), help="mafft alignment output format (default=%(default)s)", default="fasta")
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

clustalout = bool(args.format == "clustalout")
mafft_cline = MafftCommandline(input=args.input, clustalout=clustalout)
stdout, stderr = mafft_cline()

with open(args.output, "w", encoding="ascii") as alignment_file:
    alignment_file.write(stdout)

with open(args.error, "w", encoding="ascii") as report_file:
    report_file.write(stderr)
