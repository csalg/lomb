import time
from os import path

import numpy as np
import pandas as pd
from flask import current_app
from sklearn.linear_model import LinearRegression
import pickle

from config import DATAPOINTS, MAX_ELAPSED
from lib.db import get_db

MU_MAX = 10e10
MU_MIN = 10e-10

class MTR:
    def __init__(self):
        self.model = LinearRegression
        self.column_names = []

    def load(self):
        with open('src/slices/probabilities/model.pkl', 'rb') as file:
            self.model = pickle.load(file)

        with open('src/slices/probabilities/column_names.pkl', 'rb') as file:
            self.column_names = pickle.load(file)

    def predict_to_df(self, df):
        X = df[self.column_names]
        X = engineer_features(X)
        now = int(time.time())
        mu_pred = self.model.predict(X)
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


def engineer_features(X):
    for feature_name in X.columns:
        if 'seconds' in feature_name:
            mask = X[feature_name].where(X[feature_name]<MAX_ELAPSED)
            inverse = np.clip(np.divide(1.0, mask), 10e-10, 10e-6)
            log_inverse = np.log(inverse)
            X[feature_name+"_inverse"] = np.nan_to_num(inverse)
            X[feature_name+"_log_inverse"] = np.nan_to_num(log_inverse)
            if 'FIRST_EXPOSURE' in feature_name:
                continue
            X.drop(feature_name, axis=1, inplace=True)
        if 'amount' in feature_name:
            X[feature_name+"_sqrt"] = np.sqrt(X[feature_name])
    return X


mtr = MTR()
mtr.load()

db = get_db()
repo = db[DATAPOINTS]

def predict_scores_for_user(username):
    datapoints_cursor = repo.find({'user': username})
    datapoints = list(map(lambda entry: {'index': f"{entry['source_language']}_{entry['lemma']}", **(entry['features']), 'timestamp': entry['timestamp']}, datapoints_cursor))
    df = pd.DataFrame(datapoints)
    df.set_index('index', inplace=True)
    return mtr.predict_to_df(df)