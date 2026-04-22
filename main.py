from fastapi import FastAPI
import subprocess
import pysam
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000"
]

def edit_vcf(new_chrom, new_pos, new_ref, new_alt):
    vcf_in = pysam.VariantFile("/data/synthetic_usecases_4beacon_testingV4.vcf")
    vcf_out = pysam.VariantFile("/data/final.vcf", 'w', header=vcf_in.header)

    for record in vcf_in:
        record.pos = new_pos
        record.ref = new_ref
        record.alts = (new_alt,)
        record.chrom = new_chrom   
        
        vcf_out.write(record)

    vcf_in.close()
    vcf_out.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/liftover")
async def liftover(pos: int, refBases: str, altBases: str, chr: str, finalAssembly: str):
    f = open("/data/result.txt", "w")
    g = open("/data/logs.txt", "w")
    edit_vcf(chr, pos, refBases, altBases)
    if finalAssembly == 'GRCh38':
        result = subprocess.run(
            ["bcftools", "+liftover", "/data/final.vcf", "--", "-s", "/data/GRCh37-lite.fa", "-f", "/data/GRCh38_full_analysis_set_plus_decoy_hla.fa",  "-c", "/data/hg19ToHg38.over.chain.gz"],
            stdout=f,
            stderr=g
        )
    elif finalAssembly == 'GRCh37':
        result = subprocess.run(
            ["bcftools", "+liftover", "/data/final.vcf", "--", "-s", "/data/GRCh38_full_analysis_set_plus_decoy_hla.fa", "-f", "/data/GRCh37-lite.fa", "-c", "/data/hg38ToHs1.over.chain.gz"],
            stdout=f,
            stderr=g
        )
    with open('/data/logs.txt', 'r') as g:
        liftover = g.readlines()[-1]
        if 'Error' in liftover:
            return {"error": liftover}
        split_by_slash=liftover.split('/')
        rejected=int(split_by_slash[-1])
        reference_added=int(split_by_slash[-2])
        swapped=int(split_by_slash[-3])
        total=int(split_by_slash[-4].split(':')[-1])
    with open('/data/result.txt', 'r') as f:
        liftover = f.readlines()[-1]
        split_by_tab=liftover.split('\t')
        chr=split_by_tab[0]
        pos=split_by_tab[1]
        ref=split_by_tab[3]
        alt=split_by_tab[4]
    return {"chr": chr, "pos": pos, "ref": ref, "alt": alt, "total": total, "swapped":swapped,"reference added": reference_added, "rejected": rejected }