import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from easyenergy.callbacks.keras import TrainCallback
from easyenergy.callbacks.keras import PerEpochCallback
from easyenergy.callbacks.keras import PredictCallback


data = pd.read_csv('crypto_tradinds_100000.csv')
btc_data = data[data['ticker'] == 'BTC']
btc_data_0 = btc_data[data['price_btc'] == 0]
drop_columns_list = btc_data.nunique()[btc_data.nunique() <= 2].index
btc_data.drop(drop_columns_list, axis=1, inplace=True)


def data_preproc_and_split(data, n):
    col = []

    for i in range(n):
        col.append('price' + str(i))
        col.append('volume' + str(i))

    train = pd.DataFrame(columns=col)
    target = pd.DataFrame(columns=['date', 'price'])
    pred_convert = pd.DataFrame(columns=['date', 'price'])

    # Preprocessing of data
    for i in range(1, len(data)-n-1):
        def_nom = data.loc[i-1, 'price_usd']

        for j in range(n):
            train.loc[i, 'price' + str(j)] = data.loc[i+j,
                                                      'price_usd']/def_nom-1
            vstr = 'volume' + str(j)
            train.loc[i, vstr] = data.loc[i+j, 'volume']/data.loc[i+j,
                                                                  'market_cap']

        target.loc[i, 'price'] = data.loc[i+n+1, 'price_usd']/def_nom-1
        target.loc[i, 'date'] = data.loc[i+n+1, 'trade_date']
        # Save start prices for convertation prediction resalt to valid prices
        pred_convert.loc[i, 'price'] = def_nom
        pred_convert.loc[i, 'date'] = data.loc[i+n+1, 'trade_date']

    # Data split
    x_train = train.iloc[:train.shape[0]-100]
    x_valid = train.iloc[train.shape[0]-100:]
    y_train = target.iloc[:target.shape[0]-100]
    y_valid = target.iloc[target.shape[0]-100:]
    y_train.drop(['date'], axis=1, inplace=True)
    y_valid.drop(['date'], axis=1, inplace=True)

    # Convert shape of data for LSTM model
    x_train = x_train.to_numpy().reshape((x_train.shape[0], n, 2))
    x_valid = x_valid.to_numpy().reshape((x_valid.shape[0], n, 2))
    return x_train, x_valid, y_train, y_valid, target, pred_convert


n = 25  # chunk from the dataset used to train the model
x, x_val, y, y_val, target, pred_convert = data_preproc_and_split(btc_data, n)

x = np.asarray(x).astype('float32')
y = np.asarray(y).astype('float32')
x_val = np.asarray(x_val).astype('float32')
y_val = np.asarray(y_val).astype('float32')


model = Sequential()
model.add(LSTM(32,
               return_sequences=True, input_shape=(25, 2)))
model.add(LSTM(64))
model.add(Dropout(0.1))
model.add(Dense(128, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')


def test_traincallback():

    cb1 = TrainCallback()
    model.fit(x, y,
              batch_size=512,
              validation_data=(x_val, y_val),
              epochs=25, shuffle=False, verbose=2,
              callbacks=[cb1])
    model.save('bitcoin_model.h5')


def test_perepochcallback():
    cb = PerEpochCallback()
    model.fit(x, y,
              batch_size=512,
              validation_data=(x_val, y_val),
              epochs=2, shuffle=False, verbose=2,
              callbacks=[cb])


def test_predictcallback():
    model = load_model('bitcoin_model.h5')
    cb2 = PredictCallback()
    model.predict(x_val, callbacks=[cb2])


test_traincallback()
test_perepochcallback()
test_predictcallback()
