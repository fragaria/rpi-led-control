FROM python:3.6-slim

EXPOSE 5000

# Install gunicorn
RUN pip install gunicorn

# Install falcon
RUN pip install falcon

RUN apt-get update && apt-get install -y build-essential python-dev

RUN pip install RPi.GPIO
RUN pip install apa102-pi

# Add demo app
COPY ./server.py /server.py
WORKDIR /

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--capture-output","server:app"]

