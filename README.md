 docker run --rm -v /test:/mnt -w /mnt dbest/mafft:latest msa.py -i Sequences.fa -o msa.out -s blastn -n 1 -a 1