import numpy as np
from sklearn.linear_model import LinearRegression
import pickle


MU_MAX = 10e10
MU_MIN = 10e-10



class MTR:
    def __init__(self):
        self.model = LinearRegression
        self.column_names = []

    def load(self):
        with open('model.pkl', 'rb') as file:
            self.model = pickle.load(file)

        with open('column_names.pkl', 'rb') as file:
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

def predict_score(df):
    return mtr.predict_to_df(df)