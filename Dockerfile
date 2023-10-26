FROM python:3.11-slim

WORKDIR /work
COPY ./requirements.txt /work/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /work/requirements.txt \
    && cd .. \
    && rm -rf /work

COPY . /app
WORKDIR /app
RUN rm -rf ./dev ./log .gitignore ./.git requirements.txt
CMD uvicorn module.server:app --host 0.0.0.0 --port 17680 --log-level critical
