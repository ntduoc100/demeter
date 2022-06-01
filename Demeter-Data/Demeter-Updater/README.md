# Updater component
## Functionality
- Realtime weather data crawling (5 min interval).Data are stored in realtime_data
- Occasional weather data crawling (30 min interval). Data are stored in historical_data
## Testing
- Uncomment connection string in ```Testing``` block of ```runner.py``` and ```region_data.py``` and comment the one which is outside of the block
- Pull MongoDB image from DockerHub

```docker pull mongo```

- Build an image named demeter-updater 

```docker build -t demeter-updater .```

- Compose application

```docker compose up```

- To view database on MongoDB Compass, enter this URL: 

```mongodb://localhost:27017```

## More data sources
- Create modules that used to process data from the source
- Follow the instructions from ```runner.py```, ```Dockerfile```  to integrate the module

## Deploy
- To deploy this components, only use ```Dockerfile``` to build model and follow the instructions provided by the deployment platform