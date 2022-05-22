# Multiple Parallel Input and Multi-Step Output
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import Dropout
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
N_STEPS_IN, N_STEPS_OUT, N_STEPS = 1440, 336, 6
LEARNING_RATE = 0.001
EPOCHS = 2
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

    df = df.dropna()

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

    Return:
    - Trained model
    '''
    # Check for model existence
    if os.path.exists('models/' + model_name):
        model = keras.models.load_model('models/' + model_name)

    else:
        model = Sequential()
        model.add(LSTM(300, activation='tanh', input_shape=(
            int(N_STEPS_IN/N_STEPS), N_FEATURES)))
        model.add(RepeatVector(int(N_STEPS_OUT/N_STEPS)))
        model.add(Dropout(0.2))
        model.add(LSTM(300, activation='tanh', return_sequences=True))
        model.add(TimeDistributed(Dense(N_FEATURES)))
        model.compile(optimizer=keras.optimizers.Adam(
            learning_rate=LEARNING_RATE), loss='mse')
    
    # fit model
    model.fit(X, y, epochs=EPOCHS, verbose=True)

    shutil.rmtree('models/' + model_name, ignore_errors=True)
    model.save('models/' + model_name)

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
        print(loc)
        # Check if model exists
        model_name = loc.replace(' ','_')
        if os.path.exists('models/' + model_name):
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
            this_month = datetime.now()
            last_month = this_month - relativedelta(months=1)

            cursor = collection.find({'$and': 
            [
                {'$or':[
                    {'Time':  {'$regex': f'2022-{last_month.strftime("%m")}.+'}},
                    {'Time': {'$regex': f'2022-{this_month.strftime("%m")}.+'}}
                    ]
                }, 
                {'Place': 'Ho Chi Minh city'}
            ]
            }, {'_id': False, 'Place': False})

        # Prepare data
        data = [i for i in cursor]
        if len(data) < N_STEPS_IN + N_STEPS_OUT:
            continue

        if have_model == True:
            data = data[-N_STEPS_IN - N_STEPS_OUT:]
        features, sc = preprocess(data)

        # Store normalizer to denormalize later
        SCs[loc] = sc

        # Convert data to past-future data points
        X, y = split_sequences(features, N_STEPS_IN, N_STEPS_OUT, N_STEPS)

        # Train
        model = fit_lstm(X, y, model_name=loc.replace(' ', '_'))



def predictor(places, collname, db):
    
    # Get collection
    collection = db.get_collection(collname)

    for loc in places:
        have_model = False
        model_name = loc.replace(' ','_')
        if os.path.exists('models/' + model_name):
            have_model = True
        else:
            continue
        
        this_month = datetime.now()
        last_month = this_month - relativedelta(months=1)

        cursor = collection.find({'$and': 
        [
            {'$or':[
                {'Time':  {'$regex': f'2022-{last_month.strftime("%m")}.+'}},
                {'Time': {'$regex': f'2022-{this_month.strftime("%m")}.+'}}
                ]
            }, 
            {'Place': 'Ho Chi Minh city'}
        ]
            }, {'_id': False, 'Place': False})

        data = [i for i in cursor]
        
        features, SCs[loc] = preprocess(data)
        
        model = keras.models.load_model('models/' + model_name)
        res = model.predict(features[-N_STEPS_IN::N_STEPS].reshape(-1, int(N_STEPS_IN/N_STEPS), N_FEATURES))

        
        preds = SCs[loc].inverse_transform(res[0])
        preds = pd.DataFrame(np.round(preds, 0)).astype('int16')
        preds.columns = ['Temperature', 'Wind', 'Humidity', 'Pressure']
        
        latest_time = datetime.strptime(data[-1]['Time'], "%Y-%m-%dT%H:%M:%S")
        if latest_time.minute == 30 :
            latest_time = latest_time - timedelta(minutes=30)
        
        time_col = []
        for _ in range(len(res)):
            time_col = latest_time + timedelta(hours=3)
            latest_time += timedelta(hours=3)
        preds['Time']  = time_col

        preds.to_csv(model_name)
        

        

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


    train_model(places, 'historical_data', db)
    predictor(places, 'historical_data', db)

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
