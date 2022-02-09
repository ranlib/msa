FROM ubuntu:latest
RUN apt-get update --yes
RUN apt-get install --yes python3 python-is-python3 python3-biopython mafft
COPY ./mafft.py /usr/local/bin/
COPY ./blast.py /usr/local/bin/
COPY ./msa.py /usr/local/bin/

