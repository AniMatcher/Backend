FROM python:3.11-slim-buster

COPY ["pyproject.toml", "poetry.lock", ".env"] 

RUN apt-get update && \
    apt-get install -y gcc && \
    python3 -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi && \
    pip3 install uvloop

COPY . .

COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./app /app
WORKDIR /
ENV PYTHONPATH=/app


EXPOSE 5000

CMD ["/start.sh"]