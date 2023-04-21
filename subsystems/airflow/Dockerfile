FROM apache/airflow:2.5.1

RUN pip install loguru==0.6.0

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         heimdal-dev gcc nano \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
