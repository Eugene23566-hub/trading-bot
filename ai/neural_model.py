# ai/neural_model.py

import tensorflow as tf
import numpy as np
import json
import os

MODEL_PATH = "data/nn_model.h5"
LOG_FILE = "data/trade_history.json"

def load_trade_data():
    if not os.path.exists(LOG_FILE):
        return None, None
    with open(LOG_FILE, 'r') as f:
        trades = json.load(f)

    X, y = [], []
    for t in trades:
        if None in (t["rsi"], t["ema"], t["macd"]):
            continue
        X.append([t["rsi"], t["ema"], t["macd"]])
        y.append(1 if t["profit"] > 0 else 0)
    return np.array(X), np.array(y)

def train_neural_model():
    X, y = load_trade_data()
    if X is None or len(X) < 50:
        return None

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(3,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=20, verbose=0, batch_size=8)
    model.save(MODEL_PATH)
    return model

def load_neural_model():
    if os.path.exists(MODEL_PATH):
        return tf.keras.models.load_model(MODEL_PATH)
    return None

def predict_with_nn(model, indicators):
    x = np.array([[indicators["rsi"], indicators["ema"], indicators["macd"]]])
    proba = model.predict(x, verbose=0)[0][0]
    return 1 if proba > 0.5 else 0, proba
