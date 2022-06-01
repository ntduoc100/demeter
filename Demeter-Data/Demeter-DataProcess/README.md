# Data Processing for Weather

A branch in [Demeter Weather](https://github.com/ntduoc100/demeter), used to crawl data, preprocess, update, train and predict for a weather project.

For public branch to use Github Actions, please access [Public-DataProcess](https://github.com/huutuan122/test-crawl)

# Description

- `dataCollecting.py` used to collect data from free.meteo.com
- `dataPreprocessing.py` used to clean data, save them to a folder.
- `dataUploading.py`used to upload data to mongoDB server.
- `dataModelling.py` used to train model, find the best coefficient for predicting phase.
- `dataPredicting.py` used to forecast weather for each province in VietNam.
- `./github/workflow`: Each file in this foler will run each time you commit. To disable this, go to `Action` and choose the file you want to disable. Then, click Disable workflow`
  - `crawlData.yml`: used to crawl data using github action. To run this, go to `Action` and click `Enable workflow`
  - `getCoefficient.yml`: used to automatically get coefficient. This file run automatically each weak.
  - `automaticallyPredict.yml`: used to automatically predict. This file run automatically each hour.

# How to run

- To run each file, command: `python3 [filename] --help` for more information
- View `".github"` folder for the sample command
- Find the version of library that being used, and save them to `requirements.txt`
- To run this project, follow my steps:

  - First, run 3 files `dataCollecting.py `, `dataPreprocessing.py `and `dataUploading.py` step by step, which was specified in './github/workflows/crawlData.yml'
  - Next, run `dataModelling.py` to get coefficient for model, which was used in the next phase, which was specified in './github/workflows/getCoefficient.yml'.
  - Finally, run `dataPredicting.py` to forecast weather data, which was specified in './github/workflows/automaticallyPredict.yml'.

# License

Demeter team - Grab VietNam's Tech Bootcamp 2022
