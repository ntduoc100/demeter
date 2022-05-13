FROM python:3.9

WORKDIR /code
COPY update_weather.py update_weather.py
COPY region_data.py region_data.py
COPY requirements.txt requirements.txt
COPY run.sh run.sh
RUN chmod +x run.sh
RUN pip3 install -r requirements.txt

ENTRYPOINT ["./run.sh"]