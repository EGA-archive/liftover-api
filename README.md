# liftover-api

Welcome to the liftover API from EGA. This software is relying on [score](https://software.broadinstitute.org/software/score/) files for the liftover plugin for BCFTools developed [here](https://github.com/freeseek/score).

Wrapped in a Dockerized container, the software runs through an API request.

## How to deploy

You will need to download the following files inside data folder:
- hg38ToHs1.over.chain.gz
- hg19ToHg38.over.chain.gz
- GRCh38_full_analysis_set_plus_decoy_hla.fa
- GRCh37-lite.fa

Once you have all the needed files, run the followimg command to deploy the liftover api:

```bash
docker compose up -d --build
```

## How to use

Go to http://localhost:7000 and start making liftover queries:

```bash
http://localhost:7000/liftover?pos=19653341&refBases=AT&altBases=A&chr=21&finalAssembly=GRCh38
```


