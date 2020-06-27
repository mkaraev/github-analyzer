FROM python:3.7.1

COPY requirements.txt /opt/analyzer/requirements.txt
RUN pip install -r /opt/analyzer/requirements.txt

ADD . /opt/analyzer
WORKDIR /opt/analyzer
