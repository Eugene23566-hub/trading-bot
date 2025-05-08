# ai/model_trainer.py

import json
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

DATA_PATH = "data/trade_history.json"
MODEL_PATH = "data/model.pkl"

def load_trade_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    with open(DATA_PATH, 'r') as f:
        trades = json.load(f)
    return pd.DataFrame(trades)

def train_model():
    df = load_trade_data()
    if df.empty or len(df) < 20:
        return None

    df = df.dropna()
    df['success'] = df['profit'].apply(lambda x: 1 if x > 0 else 0)
    X = df[['rsi', 'ema', 'macd']]
    y = df['success']

    model = LogisticRegression()
    model.fit(X, y)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    return model

def predict_signal(model, indicators: dict):
    X_test = [[indicators['rsi'], indicators['ema'], indicators['macd']]]
    proba = model.predict_proba(X_test)[0][1]
    signal = model.predict(X_test)[0]
    return signal, proba
