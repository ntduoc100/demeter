# Multiple Parallel Input and Multi-Step Output
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from tensorflow import keras
import pandas as pd
import pymongo
from sklearn.preprocessing import MinMaxScaler
import os
import shutil
import threading as th
import signal
import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

SCs = dict()

# Tuning variables
N_STEPS_IN, N_STEPS_OUT, N_STEPS = 1440, 366, 6
LEARNING_RATE = 0.001
EPOCHS = 20
N_FEATURES = 4

class Job(th.Thread):
    '''
    Description:
    - Create thread job that run forever
    '''

    def __init__(self, name, worker, runner, interval=0.5, **kwargs):
        '''
        Parameters:
        - worker: function where the code should be run in the thread
        - interval: amount of time between executions
        - runner: function that wrap the worker with additional code
        '''
        th.Thread.__init__(self)

        self.shutdown_flag = th.Event()
        self.worker = worker
        self.interval = interval
        self.runner = runner
        self.kwargs = kwargs
        self.name = name

    def run(self):
        while not self.shutdown_flag.is_set():
            # Job code
            self.runner(self.worker, self.interval, **self.kwargs)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    '''Raise exception to stop the program when a terminate signal received'''
    raise ServiceExit


def get_db(connection_str):
    '''Description:
    - Establish connection to database and return a database instance
    '''
    client = pymongo.MongoClient(connection_str)
    db = client.get_database('demeter')
    return db

class trainer:
    def __init__(self):
        self.SCs = dict()

    
def preprocess(data: list):
    '''
    Parameters:
    - data (json): raw data 

    Description: 
    - Fill nan
    - Sort by date
    - Select feature columns
    - Normalize

    Return:
    - df (pandas dataframe): processed data
    - scaler: Normalizer
    '''
    df = pd.json_normalize(data)

    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values(by='Time', ascending=True)
    # Ensure that the last timestamp is not a half of an hour
    if df['Time'].max().minute == '30':
        df.drop([df.index[-1]])

    # Fill nan to not interfere with the timeline
    df.fillna(df.mean())

    df = df.drop(columns='Time')
    df = df.reset_index(drop=True)

    sc = MinMaxScaler((0, 1))
    features = sc.fit_transform(df)

    return features, sc


def split_sequences(sequences, N_STEPS_IN, N_STEPS_OUT, N_STEPS):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + N_STEPS_IN
        out_end_ix = end_ix + N_STEPS_OUT
        # check if we are beyond the dataset
        if out_end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix:N_STEPS,:], sequences[end_ix:out_end_ix:N_STEPS, :]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def fit_lstm(X, y, model_name):
    '''
    Parameters:
    - X: train data
    - y: label
    - model_name: name of the model
    - EPOCHS: number of EPOCHS
    - N_FEATURES: number of features
    - N_STEPS_IN: number of data point in the past
    - N_STEPS_OUT: number of data point in the future
    - N_STEPS: number of time steps

    Description:
    - Create an lstm model to fit the time series
    - If old models exists, load them and continue the training on new data

    Return:
    - Trained model
    '''
    # Check for model's existence
    if os.path.exists('model/' + model_name):
        model = keras.models.load_model('model/' + model_name)

    else:
        model = Sequential()
        model.add(LSTM(300, activation='tanh', input_shape=(
            int(N_STEPS_IN/N_STEPS), N_FEATURES)))
        model.add(RepeatVector(int(N_STEPS_OUT/N_STEPS)))
        model.add(LSTM(300, activation='tanh', return_sequences=True))
        model.add(TimeDistributed(Dense(N_FEATURES)))
        model.compile(optimizer=keras.optimizers.Adam(
            learning_rate=LEARNING_RATE), loss='mse')
    
    # fit model
    model.fit(X, y, epochs=EPOCHS, verbose=True)

    shutil.rmtree('model/' + model_name, ignore_errors=True)
    model.save('model/' + model_name)

    return model


def train_model(places, collname, db):
    '''
    Description:
    - Split data into multiples past-future data points
    - Looks at the 1 month in the past, predict next 7 days
    - The data is recorded each 30 minutes
    - Number of timestamps to the past should be 30*24*2 = 1440
    - Number of timestamps to the future should be 8*24*2 = 366 
    - Assume that there is no significant change every 3 hours
    - Time steps should be 6

    Returns:
    - Normalizer
    '''


    # Get collection
    collection = db.get_collection(collname)

    # Train model for each place
    for loc in places:
        have_model = False

        # Check if model exists
        if len(os.listdir('model')) == 0:
            have_model = True

        if have_model == False:
        # Train model the most 2 recent years data
            cursor = collection.find({'$and': 
            [
                {'$or':[
                    {'Time':  {'$regex': '2022.+'}},
                    {'Time': {'$regex': '2021.+'}}
                    ]
                }, 
                {'Place': loc}
            ]
                }, {'_id': False, 'Place': False})
        else:
            # Model existed train: last month
            this_month = datetime.now().month
            cursor = collection.find({'$and': 
            [
                {'$or':[
                    {'Time':  {'$regex': f'2022-{this_month - 1}.+'}},
                    {'Time': {'$regex': f'2022-{this_month}.+'}}
                    ]
                }, 
                {'Place': loc}
            ]
                }, {'_id': False, 'Place': False})

        # Prepare data
        data = [i for i in cursor]
        if len(data) < 1440:
            continue

        if have_model == True:
            data = data[-1440:, :]
        features, sc = preprocess(data)

        # Store normalizer to denormalize later
        SCs[loc] = sc

        # Convert data to past-future data points
        X, y = split_sequences(features, N_STEPS_IN, N_STEPS_OUT, N_STEPS)

        # Train
        model = fit_lstm(X, y, model_name=loc.replace(' ', '_'))


def predict_weather(places, collname, db):
    '''
    Parameters:
    - Places: list of data about places
    - collname: collection name
    - db: data base
    Desciptions:
    - Data 
    '''
    # Get collection
    collection = db.get_collection(collname)

    for loc in places:
        have_model = False
        model_name = loc.replace(' ','_')
        if os.path.exists('model/' + model_name):
            have_model = True
        else:
            continue
        
        now = datetime.now()
        last_month = now - relativedelta(months=1)
        this_year = now.strftime("%Y")

        # Get data from last month
        cursor = collection.find({'$and': 
        [
            {'$or':[
                {'Time':  {'$regex': f'{this_year}-{last_month.strftime("%m")}.+'}},
                {'Time': {'$regex': f'{this_year}-{now.strftime("%m")}.+'}}
                ]
            }, 
            {'Place': 'Ho Chi Minh city'}
        ]
            }, {'_id': False, 'Place': False})

        # Pack data to list and preprocess
        data = [i for i in cursor]
        features, sc = preprocess(data)
        

        # Predict
        model = keras.models.load_model('model/' + model_name)
        res = model.predict(features[-N_STEPS_IN::N_STEPS].reshape(-1, int(N_STEPS_IN/N_STEPS), N_FEATURES))

        
        preds = sc.inverse_transform(res[0])
        preds = pd.DataFrame(np.round(preds, 0)).astype('int16')
        preds.columns = ['Temperature', 'Wind', 'Humidity', 'Pressure']
        
        latest_time = datetime.strptime(data[-1]['Time'], "%Y-%m-%dT%H:%M:%S")
        
        # Keep the data
        if latest_time.minute == 30 :
            latest_time = latest_time - timedelta(minutes=30)
        
        time_col = []
        for _ in range(len(res)):
            time_col = latest_time + timedelta(hours=3)
            latest_time += 3
        preds['Time']  = time_col

        # TODO:
        # - Convert dataframe to json
        # - Update predicted data to database
        

def job_runner(worker, interval, **kwargs):
    time.sleep(interval)
    worker(kwargs['collection'])


if __name__ == '__main__':

    connection_str = 'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    db = get_db(connection_str)

    # Check for collections existence
    if 'historical_data' not in db.list_collection_names() or 'region_data' not in db.list_collection_names():
        raise Exception('Collections not found')

    # List of recorded places
    cursor = db.get_collection('region_data').find(
        {}, {'Place': True, '_id': False})

    # Get places
    places = pd.json_normalize([i for i in cursor])['Place']

    # Get training data

    # TODO:
    # - Add threading mechanism
    # - A thread for training
    # - A thread for predicting
    
    train_model(places, 'historical_data', db)
    predict_weather(places, 'historical_data', db)

    # Register signals
    # signal.signal(signal.SIGTERM, service_shutdown)
    # signal.signal(signal.SIGINT, service_shutdown)

    # try:
    #     trainer = Job(
    #         'trainer',
    #         train_model,
    #         job_runner,
    #         604800, # 1 week
    #         collection=collection
    #     )

    #     trainer.start()

    #     # Keep the program alive
    #     while True:
    #         time.sleep(0.5)

    # except ServiceExit:
    #     trainer.shutdown_flag.set()

    #     # Wait for the threads to close...
    #     trainer.join()
