FROM broadinstitute/gatk:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV BCFTOOLS_PLUGINS=/opt/bcftools/plugins
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    wget \
    unzip \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    fastapi \
    uvicorn[standard]

RUN mkdir -p /opt/bcftools/plugins

RUN wget -q -O /tmp/score.zip \
    https://software.broadinstitute.org/software/score/score_1.20-20240505.zip \
 && unzip -q /tmp/score.zip -d /tmp/score \
 && find /tmp/score -name "*.so" -exec cp {} /opt/bcftools/plugins/ \; \
 && rm -rf /tmp/score /tmp/score.zip

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/opt/gatk/lib:$LD_LIBRARY_PATH

WORKDIR /app

COPY main.py /app/main.py

EXPOSE 7000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]