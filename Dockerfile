FROM jupyter/minimal-notebook:latest

COPY requirements.txt .
COPY demo.ipynb .
COPY demohelpers.py .

RUN pip3 install -r requirements.txt