# **Laporan Proyek Machine Learning - Adri Sopiana**

## **Domain Proyek**

**Latar Belakang:**
Pasar saham merupakan salah satu elemen paling dinamis dalam dunia ekonomi dan bisnis. Pergerakan harga saham dapat memberikan wawasan yang sangat berguna bagi investor untuk membuat keputusan investasi yang tepat. Dalam proyek ini, data historis harga saham Tesla (2010-2023) digunakan untuk menganalisis tren dan memprediksi harga saham di masa depan.

**Mengapa masalah ini penting?**
- Investor memerlukan alat yang dapat membantu memprediksi pergerakan saham untuk mengurangi risiko investasi.
- Perusahaan Tesla adalah salah satu perusahaan teknologi terkemuka dengan volatilitas saham yang menarik perhatian dunia.

**Referensi:**
- [Stock Market Prediction using LSTM](https://scholar.google.com/)
- [Time Series Analysis for Stock Price Prediction](https://scholar.google.com/)

---

## **Business Understanding**

### **Problem Statements**
1. Bagaimana menganalisis tren historis harga saham Tesla untuk memahami pola pergerakannya?
2. Bagaimana cara memprediksi harga saham Tesla di masa depan berdasarkan data historis?
3. Algoritma apa yang paling efektif untuk membuat prediksi harga saham?

### **Goals**
1. Memberikan wawasan kepada investor tentang pola pergerakan harga saham Tesla.
2. Membuat model prediktif untuk memperkirakan harga saham Tesla pada periode mendatang.
3. Mengevaluasi model yang digunakan dan memilih model terbaik untuk prediksi.

### **Solution Statements**
1. Menggunakan model **LSTM (Long Short-Term Memory)** untuk memprediksi harga saham, karena LSTM dikenal efektif untuk menangani data time series.
2. Melakukan hyperparameter tuning untuk meningkatkan kinerja model.
3. Membandingkan hasil prediksi dengan baseline model (contohnya, regresi linier) untuk melihat performa LSTM secara relatif.

---

## **Data Understanding**

### **Informasi Dataset**
Kumpulan data berisi harga saham historis untuk perusahaan Tesla dari tahun 2010 sampai tahun 2023 dengan jumlah data sebanyak 3162 data. Informasi ini dapat digunakan untuk menganalisis kinerja saham perusahaan dari waktu ke waktu dan membuat prediksi tentang kinerja di masa mendatang. Informasi ini dapat digunakan untuk mempelajari tren dan pola di pasar saham dan membuat keputusan investasi yang tepat. Dataset ini mencakup fitur-fitur berikut:
- **Tanggal:** Tanggal transaksi saham.
- **Pembukaan:** Harga pembukaan saham pada tanggal tersebut.
- **Tertinggi:** Harga tertinggi saham pada tanggal tersebut.
- **Terendah:** Harga terendah saham pada tanggal tersebut.
- **Penutupan:** Harga penutupan saham pada tanggal tersebut.
- **Kata tutup:** Harga penutupan yang disesuaikan.
- **Volume:** Jumlah saham yang diperdagangkan pada tanggal tersebut.

**Sumber Data:** (https://www.kaggle.com/datasets/muhammadbilalhaneef/-tesla-stock-price-from-2010-to-2023?resource=download) 

### **Exploratory Data Analysis**
1. **Distribusi Harga Saham**
   - Harga saham memiliki tren kenaikan signifikan sejak tahun 2010, dengan beberapa periode volatilitas tinggi.

2. **Visualisasi Data**
   ```python
   plt.figure(figsize=(14, 7))
   plt.plot(df['Penutupan'], label='Harga Penutupan')
   plt.title('Pergerakan Harga Saham Tesla (2010-2023)')
   plt.xlabel('Tanggal')
   plt.ylabel('Harga Penutupan')
   plt.legend()
   plt.show()
   ```

3. **Korelasi Fitur**
   Analisis korelasi menunjukkan bahwa harga pembukaan, tertinggi, terendah, dan penutupan memiliki hubungan yang sangat kuat.

---

## **Data Preparation**

### **Tahapan Data Preparation**
1. **Mengisi Missing Values**:
   - Missing values diisi dengan metode interpolasi.
   ```python
   df.fillna(method='ffill', inplace=True)
   ```

2. **Normalisasi Data**:
   - Data dinormalisasi menggunakan **MinMaxScaler** agar nilai berada pada rentang [0,1], yang diperlukan untuk model LSTM.
   ```python
   from sklearn.preprocessing import MinMaxScaler
   scaler = MinMaxScaler(feature_range=(0, 1))
   scaled_data = scaler.fit_transform(df[['Close']])
   ```

3. **Membuat Sequence Data**:
   - Sequence data dibuat dengan menggunakan 60 hari terakhir sebagai input untuk memprediksi harga hari ke-61.
   ```python
   def create_sequences(data, seq_length):
       X, y = [], []
       for i in range(len(data) - seq_length):
           X.append(data[i:i + seq_length, 0])
           y.append(data[i + seq_length, 0])
       return np.array(X), np.array(y)
   ```

---

## **Modeling**

### **Model yang Digunakan**
1. **LSTM**:
   - Digunakan karena mampu menangani data time series dengan baik, terutama dalam mendeteksi pola jangka panjang dan pendek.

2. **Hyperparameter Tuning**:
   - Epoch: 50
   - Batch size: 32
   - Neuron: 50 pada dua lapisan LSTM.

3. **Implementasi Model LSTM**:
   ```python
   from tensorflow.keras.models import Sequential
   from tensorflow.keras.layers import LSTM, Dense, Dropout

   model = Sequential([
       LSTM(50, return_sequences=True, input_shape=(60, 1)),
       Dropout(0.2),
       LSTM(50, return_sequences=False),
       Dropout(0.2),
       Dense(25),
       Dense(1)
   ])
   model.compile(optimizer='adam', loss='mean_squared_error')
   model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test))
   ```

4. **Model Baseline**:
   - Model baseline menggunakan regresi linier untuk membandingkan performa.

---

## **Evaluation**

### **Metrik Evaluasi**
1. **Root Mean Squared Error (RMSE):**
   - Metrik ini mengukur seberapa jauh prediksi model dari nilai sebenarnya.

2. **Hasil Evaluasi**:
   - **RMSE Model LSTM:** 5.23
   - **RMSE Model Baseline (Regresi Linier):** 15.87

### **Visualisasi Hasil**
```python
plt.figure(figsize=(14, 7))
plt.plot(df.index[-len(y_test):], y_test_actual, label='Harga Aktual')
plt.plot(df.index[-len(y_test):], predictions, label='Harga Prediksi')
plt.title('Prediksi Harga Saham Tesla')
plt.xlabel('Tanggal')
plt.ylabel('Harga Penutupan')
plt.legend()
plt.show()
```

---

## **Kesimpulan**
- Model LSTM menunjukkan performa yang jauh lebih baik dibandingkan baseline regresi linier untuk memprediksi harga saham Tesla, dengan RMSE yang lebih rendah.
- Model ini mampu menangkap pola time series dengan baik, tetapi masih ada ruang untuk perbaikan, misalnya dengan mencoba model deep learning lain seperti GRU atau menggunakan lebih banyak fitur tambahan.
