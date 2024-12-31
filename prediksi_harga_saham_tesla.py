# -*- coding: utf-8 -*-
"""Prediksi Harga Saham Tesla.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16E5nChNwM9XODlcxTLhYwUWhsA1ABI1-

# Proyek Pertama: Predictive Analytics Saham Tesla (2010-2023)
Data set: https://www.kaggle.com/datasets/muhammadbilalhaneef/-tesla-stock-price-from-2010-to-2023?resource=download

# Data Loading
## Import Library
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

"""## Load Dataset"""

df = pd.read_csv("https://raw.githubusercontent.com/Adri720S/PredictiveAnalytics1_Saham-Tesla-2010-2023-/refs/heads/main/Tesla%20Stock%20Price%20(2010%20to%202023).csv")

df.head()

# Ubah kolom 'Date' menjadi tipe datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set kolom tanggal sebagai index
df.set_index('Date', inplace=True)

# Lihat info dataset
print(df.info())

"""## Visualisasi Data"""

plt.figure(figsize=(14, 7))
plt.plot(df['Close'], label='Harga Penutupan')
plt.title('Pergerakan Harga Saham Tesla (2010-2023)')
plt.xlabel('Tanggal')
plt.ylabel('Harga Penutupan')
plt.legend()
plt.show()

"""## Preprocessing Data"""

# Ambil hanya kolom harga penutupan untuk prediksi
data = df[['Close']]

# Normalisasi data untuk meningkatkan performa LSTM
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Split data menjadi training dan testing (80% train, 20% test)
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

"""## Membuat Data Sequence untuk LSTM

"""

# LSTM membutuhkan input dalam bentuk sequence (X) dan target (y)
# Fungsi untuk membuat sequence data
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length, 0])
        y.append(data[i + seq_length, 0])
    return np.array(X), np.array(y)

# Panjang sequence
seq_length = 60  # Menggunakan 60 hari terakhir untuk memprediksi

# Membuat sequence untuk training dan testing
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# Ubah bentuk data agar sesuai dengan input LSTM (samples, timesteps, features)
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

"""## Bangun Model LSTM"""

# Bangun model LSTM
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])

# Compile model
model.compile(optimizer='adam', loss='mean_squared_error')

# Latih model
history = model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test))

"""## Evaluasi dan Prediksi"""

# Prediksi menggunakan data testing
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)  # Balikkan skala ke bentuk asli

# Balikkan skala y_test ke bentuk asli
y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

# Evaluasi dengan RMSE
from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(y_test_actual, predictions))
print(f'Root Mean Squared Error (RMSE): {rmse}')

"""## Visualisasi Hasil"""

plt.figure(figsize=(14, 7))
plt.plot(df.index[-len(y_test):], y_test_actual, label='Harga Aktual')
plt.plot(df.index[-len(y_test):], predictions, label='Harga Prediksi')
plt.title('Prediksi Harga Saham Tesla')
plt.xlabel('Tanggal')
plt.ylabel('Harga Penutupan')
plt.legend()
plt.show()