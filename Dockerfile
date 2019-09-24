FROM python:3.6-slim as builder

RUN apt-get update && apt-get install -y build-essential python-dev
RUN pip install gunicorn falcon RPi.GPIO apa102-pi

RUN which gunicorn

FROM python:3.6-slim

WORKDIR /usr/src/app
COPY ./server.py server.py

COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--capture-output","server:app"]

EXPOSE 5000
