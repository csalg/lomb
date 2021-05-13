from os import path

import numpy as np
import pandas as pd
from flask import current_app
from sklearn.linear_model import LinearRegression
import pickle

from config import DATAPOINTS
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
        delta = df['delta']
        mu_pred = self.model.predict(X)
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


mtr = MTR()
mtr.load()

db = get_db()
repo = db[DATAPOINTS]

def predict_score(df):
    return mtr.predict_to_df(df)

def predict_scores_for_user(username):
    datapoints_cursor = repo.find({'user': username})
    datapoints = list(map(lambda entry: {'index': f"{entry['source_language']}_{entry['lemma']}", **(entry['features']), 'last_timestamp': entry['previous_timestamp']}, datapoints_cursor))
    df = pd.DataFrame(datapoints)
    df.set_index('index', inplace=True)
    predict_score(df)
    return df