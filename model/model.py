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


def get_db(connection_str):
    '''Description:
    - Establish connection to database and return a database instance
    '''
    client = pymongo.MongoClient(connection_str)
    db = client.get_database('demeter')
    return db


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
    df = data.copy()

    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values(by='Time', ascending=True)
    df = df.reset_index(drop=True)
    # Ensure that the last timestamp is not a half of an hour
    if df['Time'].max().minute == '30':
        df.drop([df.index[-1]])

    df = df.sort_values(by='Time')
    # Fill nan to not interfere with the timeline
    df.fillna(df.mean())

    df = df.drop(columns=['_id', 'Time', 'Place'])
    df = df.reset_index(drop=True)
    # Normalize
    sc = MinMaxScaler((0, 1))
    features = sc.fit_transform(features)

    return df, sc


def split_sequences(sequences, n_steps_in, n_steps_out, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps_in
        out_end_ix = end_ix + n_steps_out
        # check if we are beyond the dataset
        if out_end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix:n_steps,
                                 :], sequences[end_ix:out_end_ix:n_steps, :]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def training(X, y, learning_rate, model_name, epochs):
    # Check for model existence
    if os.path.exists('model/' + model_name):
        model = keras.models.load_model('model/' + model_name)
        shutil.rmtree('model/' + model_name)
    else:
        model = Sequential()
        model.add(LSTM(200, activation='tanh', input_shape=(
            int(n_steps_in/n_steps), n_features)))
        model.add(RepeatVector(int(n_steps_out/n_steps)))
        model.add(LSTM(200, activation='tanh', return_sequences=True))
        model.add(TimeDistributed(Dense(n_features)))
        model.compile(optimizer=keras.optimizers.Adam(
            learning_rate=learning_rate), loss='mse')

    # fit model
    model.fit(X, y, epochs=epochs, verbose=True)

    model.save('model/' + model_name)

    return model


if __name__ == '__main__':

    connection_str = 'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    db = get_db(connection_str)

    # Check for collections existence
    if 'historical_data' not in db.list_collection_names() or 'region_data' not in db.list_collection_names():
        raise Exception('Collections not found')

    # List of recorded places
    collection = db.get_collection('region_data').find(
        {}, {'Place': True, '_id': False})
    places = pd.json_normalize([i for i in collection])['Place']

    # Get training data
    collection = db.get_collection('historical_data')

    ########################################
    #  Traing section
    ########################################
    '''
    - Split data into multiples past-future data points
    - Looks at the 1 month in the past, predict next 7 days
    - The data is recorded each 30 minutes
    - Number of timestamps to the past should be 30*24*2 = 1440
    - Number of timestamps to the future should be 8*24*2 = 366 
    - Assume that there is no significant change every 3 hours
    - Time steps should be 6
    '''
    n_steps_in, n_steps_out, n_steps = 1440, 366, 6
    learning_rate = 0.001
    epochs = 20
    past = int(n_steps_in/n_steps)
    n_features = 4

    # Train model for each place
    for loc in places:
        # Train model the most 2 recent years data
        cursor = collection.find(
            {'$and': [
                {'Time': {'$regex': '2022.+', '$regex': '2021.+'}},
                {'Place': loc}
            ]})

        # Prepare data
        features, scaler = preprocess([i for i in cursor])

        # Convert data to past-future data points
        X, y = split_sequences(features, n_steps_in, n_steps_out, n_steps)

        model = training(X, y, learning_rate=learning_rate,
                         model_name=loc.replace(' ','_'), epochs=epochs)
