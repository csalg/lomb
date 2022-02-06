import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import tensorflow.keras as keras
import pickle

from config import MAX_ELAPSED
from db.collections import datapoint_collection

pd.options.mode.chained_assignment = None  # default='warn'

MU_MAX = 10e10
MU_MIN = 10e-10

SLICE_FOLDER = 'src/api/score_predictions'

class MTR:
    def __init__(self):
        self.model = LinearRegression
        self.column_names = []

    def load(self):
        self.model = keras.models.load_model(f'{SLICE_FOLDER}/keras_model')

        with open(f'{SLICE_FOLDER}/column_names.pkl', 'rb') as file:
            self.column_names = pickle.load(file)

        with open(f'{SLICE_FOLDER}/scaler.pkl', 'rb') as file:
            self.scaler = pickle.load(file)

    def predict_to_df(self, df):
        X_ = df[self.column_names]
        X = engineer_features(X_)
        X_scaled = self.scaler.transform(X)
        now = int(time.time())

        mu_pred_2d = np.clip(self.model.predict(X_scaled), MU_MIN, MU_MAX)
        mu_pred = mu_pred_2d.reshape(-1)
        delta = now - df['timestamp']

        df['score_pred'] = SimplifiedWickelgren.calculate_retention_rate(mu_pred, delta)

        return df


class SimplifiedWickelgren:

    @staticmethod
    def calculate_mu(retention_rate, delta):
        delta_ = delta / (24 * 60 * 60)
        retention_rate_clipped = np.clip(retention_rate, 0.1, 0.9)
        return -1. * np.divide(np.log(1 + delta_), (np.log(retention_rate_clipped)))

    @staticmethod
    def calculate_retention_rate(mu, delta):
        delta_ = delta / (24 * 60 * 60)
        mu = np.clip(mu, MU_MIN, MU_MAX)
        exponent = np.divide(-1.,mu)
        return np.power(1. + delta_, exponent)

    @staticmethod
    def get_name():
        return "SWP"


class HLRSqrt:

    @staticmethod
    def calculate_mu(retention_rate, delta):
        delta_sqrt = np.sqrt(delta)
        retention_rate_clipped = np.clip(retention_rate, 0.001, 0.999)
        term = (-1 * delta_sqrt) / np.log2(retention_rate_clipped)
        mu = np.log2(term)
        return np.clip(mu, MU_MIN + 5, MU_MAX)

    @staticmethod
    def calculate_retention_rate(mu, delta):
        delta_sqrt = np.sqrt(delta)
        mu = np.clip(mu - 5, MU_MIN, MU_MAX)
        exponent = np.divide(-1 * delta_sqrt, np.power(2., mu))
        return np.power(2., exponent)

    @staticmethod
    def get_name():
        return "HLR"


def engineer_features(X):
    for feature_name in X.columns:
        if 'seconds' in feature_name:
            mask = X[feature_name].where((0 < X[feature_name]) & (X[feature_name] < MAX_ELAPSED))

            sqrt = np.sqrt(mask)
            X.loc[:,feature_name + "_sqrt"] = np.nan_to_num(sqrt)

            inverse = np.clip(np.divide(1.0, mask), 10e-10, 10e-6)
            X.loc[:,feature_name + "_inverse"] = np.nan_to_num(inverse)

            log_inverse = np.sqrt(inverse)
            X.loc[:,feature_name + "_sqrt_inverse"] = np.nan_to_num(log_inverse)

            if 'FIRST_EXPOSURE' in feature_name:
                continue

            X.drop(feature_name, axis=1, inplace=True)
        if 'amount' in feature_name:
            X.loc[:,feature_name + "_sqrt"] = np.sqrt(X[feature_name])
            X.drop(feature_name, axis=1, inplace=True)

    return X


mtr = MTR()
mtr.load()


def predict_scores_for_user(username):
    datapoints_cursor = datapoint_collection.find({'user': username})
    datapoints = list(map(lambda entry: {
        'index': f"{entry['source_language']}_{entry['lemma']}",
        'lemma': entry['lemma'],
        'frequency': entry['frequency'] if 'frequency' in entry else 0,
        **(entry['features']),
        'timestamp': entry['timestamp']},
                          datapoints_cursor))
    df = pd.DataFrame(datapoints)
    df.set_index('index', inplace=True)
    return mtr.predict_to_df(df)
