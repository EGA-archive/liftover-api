from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/liftover")
def bcftools_version():
    result = subprocess.run(
        ["bcftools", "+liftover", "/data/synthetic_usecases_4beacon_testingV4.vcf.gz", "--", "-s", "/data/GRCh37-lite.fa", "-f", "/data/GRCh38_full_analysis_set_plus_decoy_hla.fa",  "-c", "/data/hg19ToHg38.over.chain.gz"],
        capture_output=True,
        text=True
    )
    print(result)
    return {"result": "hard-coded"}