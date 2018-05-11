# pribar

DNA primers and barcodes


### `bc25mer.240k.fasta`

240k 25-mer barcodes from Elledge lab

http://elledgelab.med.harvard.edu/?page_id=638


### `skpp15-*.faa`

PCR primer pairs (15-mers) obtained directly from Sri Kosuri (@skosuri).
Modified from Elledge barcodes.


### `skpp20-*.faa`

PCR primer pairs (20-mers) obtained from Sri Kosuri's gasp project

https://bitbucket.org/skosuri/gasp/src/ec3e33a0a942e8e751ae48d337a943a3710fec3c/ampprimers/?at=default


### `ul16-EH`

Random 16-mers generated with the following command.  They are filtered for
EcoRI and HindIII, GC content, homopolymers, Tm, and other thermo variables.

```bash
EcoRI=GAATTC
HindIII=AAGCTT

python scripts/gen-random.py -n 30000000 -l 16 \
    | python scripts/filter-site.py -s $EcoRI -s $HindIII \
    | python scripts/filter-gc.py -m 0.4 -M 0.6 \
    | python scripts/filter-quartets.py \
    | python scripts/filter-thermo.py \
        --tm-min 53.5 --tm-max 55 --ss-dg-min -4 --self-hyb-dg-min -6 \
    | python scripts/uniq.py \
    | python scripts/rename.py -p ul16-EH- -w 5 \
    > ul16-EH.fasta
```





