# Updater component
## Functionality
- Realtime weather data crawling (1 min interval).Data are stored in realtime_data
- Occasional weather data crawling (30 min interval). Data are stored in historical_data
## Testing
- Build an image named demeter-updater 

```docker build -t demeter-updater .```

- Compose application

```docker compose up```

- Data url: ```mongodb:localhost:27017```