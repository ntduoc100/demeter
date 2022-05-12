FROM python:3.9

WORKDIR /code
COPY realtime.py realtime.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "realtime.py"]