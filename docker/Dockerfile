FROM python:3.11-slim as builder

RUN apt-get update && apt-get -y install --no-install-recommends gcc libmariadb-dev pkg-config

WORKDIR /app
COPY Pipfile Pipfile.lock ./

RUN pip install -U pip && pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

FROM python:3.11-slim as runner

RUN apt-get update && apt-get -y install --no-install-recommends gcc libmariadb-dev pkg-config ca-certificates

WORKDIR /app
COPY --from=builder /app /app
COPY . /app

EXPOSE 8000

ENV PORT 8000

CMD .venv/bin/python main.py
