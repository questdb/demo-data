FROM python:3.11-slim-bookworm

# run this dockerfile from app folder
RUN addgroup --gid 10000 crypto-demo
RUN adduser --disabled-password -u 10000 --gid 10000 crypto-demo
RUN mkdir /app && chown crypto-demo:crypto-demo /app
RUN apt-get update && apt-get install -y gcc g++

USER crypto-demo

WORKDIR /app

COPY --chown=crypto-demo:crypto-demo . .

ENV PATH=$PATH:/home/crypto-demo/.local/bin
RUN pip install poetry
RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "demo_questdb.py"]
