FROM python:3.9

WORKDIR /code

# Add a package for each data source here
ADD openweathermap /code/openweathermap

# Requirement
# Add modules requirements in this file
COPY requirements.txt requirements.txt

# Please don't change this
COPY runner.py runner.py
COPY region_data.py region_data.py
COPY run.sh run.sh
RUN chmod +x run.sh
RUN pip3 install -r requirements.txt
RUN chmod a+x run.sh

ENTRYPOINT ["./run.sh"]