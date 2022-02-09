```
usage: msa.py [-h] -i INPUT [-o OUTPUT] [-s SERVICE] [-e EVALUE] [-n NHITS] [-d DATABASE] [-a ALIGNMENTS] [-f {fasta,clustalout}] [-m MSA] [-r REPORT]

msa

optional arguments:
  -h, --help                                      show this help message and exit
  -i INPUT, --input INPUT                         Fasta file with sequences
  -o OUTPUT, --output OUTPUT                      Blast results (default=results.xml)
  -s SERVICE, --service SERVICE                   Type of blast program (default=blastn)
  -e EVALUE, --evalue EVALUE                      Evalue (default=0.000000)
  -n NHITS, --nhits NHITS                         Number of hits (default=5)
  -d DATABASE, --database DATABASE                Database (default=nr)
  -a ALIGNMENTS, --alignments ALIGNMENTS          Number of alignments (default=5)
  -f {fasta,clustalout}, --format {fasta,clustalout}
                                                  mafft alignment output format (default=fasta)
  -m MSA, --msa MSA                               mafft alignment (default=mafft.out)
  -r REPORT, --report REPORT                      mafft report (default=mafft.report)


Example:

docker run --rm -v /test:/mnt -w /mnt dbest/mafft:latest msa.py -i Sequences.fa -o msa.out -s blastn -n 1 -a 1

```