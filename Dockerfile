FROM python:3.11-bookworm
LABEL maintainer="GabrielSousa02"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /proj
EXPOSE 8000

RUN set -eux; \
    apt-get clean && \
    apt-get update && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

RUN adduser --disabled-password --no-create-home \
        project-user && \
    chown -R project-user:project-user /proj

ENV PATH="/py/bin:$PATH"

USER project-user