import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set gaya seaborn
sns.set(style='darkgrid', palette='muted')

# Judul dan Deskripsi Aplikasi
st.title("Analisis Penjualan Sepeda")
st.write("""
Aplikasi ini melakukan analisis penjualan sepeda berdasarkan dataset yang mencakup informasi harian.
Analisis ini mencakup:
- RFM (Recency, Frequency, Monetary)
- Visualisasi pola penjualan berdasarkan hari dalam seminggu
- Hubungan antara temperatur dan jumlah penjualan
- Clustering menggunakan K-Means
""")

# URL dataset
DATA_URLS = {
    "day": "https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/day.csv",
    "hour": "https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/hour.csv",
}

# Memuat dataset harian
day_df = pd.read_csv(DATA_URLS["day"])

# Memeriksa kolom yang ada dalam dataset
st.subheader("Data Awal")
st.write(day_df.head())

# Filtering Data
st.sidebar.subheader("Filter Data")
rentang_temp = st.sidebar.slider("Pilih rentang temperatur (°C):", float(day_df['temp'].min()), float(day_df['temp'].max()), (0.0, 1.0))
rentang_sales = st.sidebar.slider("Pilih rentang jumlah penjualan:", int(day_df['cnt'].min()), int(day_df['cnt'].max()), (0, 100))

# Filter dataset berdasarkan input dari slider
filtered_df = day_df[(day_df['temp'] >= rentang_temp[0]) & (day_df['temp'] <= rentang_temp[1]) &
                      (day_df['cnt'] >= rentang_sales[0]) & (day_df['cnt'] <= rentang_sales[1])]

# Tampilkan data setelah filter
st.write("Data Setelah Filter:")
st.write(filtered_df)

# Analisis RFM (Recency, Frequency, Monetary)
st.subheader("Analisis RFM")
day_df['date'] = pd.to_datetime(day_df['dteday'])  # Mengubah kolom 'dteday' menjadi datetime
rfm_data = day_df.groupby('instant').agg({
    'date': 'max',  # Mengambil tanggal terakhir
    'cnt': 'sum'    # Total penjualan
}).rename(columns={'date': 'Recency'})

# Menghitung Recency
rfm_data['Recency'] = (day_df['date'].max() - rfm_data['Recency']).dt.days
rfm_data['Frequency'] = day_df.groupby('instant')['cnt'].count()  # Menghitung frekuensi
rfm_data['Monetary'] = rfm_data['cnt']  # Menggunakan total penjualan sebagai monetary

# Tampilkan Data RFM
st.write("Data RFM:")
st.write(rfm_data[['Recency', 'Frequency', 'Monetary']])

# Binning untuk Frequency dan Monetary
rfm_data['Frequency_Bin'] = pd.cut(rfm_data['Frequency'], bins=[0, 1, 5, 10, 20, 100], 
                                    labels=['1', '2-5', '6-10', '11-20', '20+'])
rfm_data['Monetary_Bin'] = pd.cut(rfm_data['Monetary'], bins=[0, 100, 200, 500, 1000, float('inf')], 
                                   labels=['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])

# Tampilkan Data RFM setelah Binning
st.write("Data RFM setelah Binning:")
st.write(rfm_data[['Recency', 'Frequency', 'Monetary', 'Frequency_Bin', 'Monetary_Bin']])

# Tombol download untuk data RFM
rfm_data_csv = rfm_data.to_csv().encode('utf-8')
st.download_button(label="Unduh Data RFM sebagai CSV", data=rfm_data_csv, file_name='rfm_data.csv', mime='text/csv')

# Visualisasi Clustering berdasarkan Monetary
plt.figure(figsize=(10, 6))
sns.countplot(data=rfm_data, x='Monetary_Bin', palette='viridis')
plt.title('Distribusi Kluster Berdasarkan Monetary', fontsize=16)
plt.xlabel('Kategori Monetary', fontsize=14)
plt.ylabel('Jumlah Pelanggan', fontsize=14)
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Pertanyaan 1: Pola Penjualan Berdasarkan Hari dalam Seminggu
st.subheader("1. Bagaimana pola penjualan bervariasi berdasarkan hari dalam seminggu?")
day_df['day_of_week'] = day_df['date'].dt.day_name()  # Mengambil nama hari
sales_by_day = day_df.groupby('day_of_week')['cnt'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

# Visualisasi jumlah penjualan berdasarkan hari
plt.figure(figsize=(10, 6))
sns.barplot(x=sales_by_day.index, y=sales_by_day.values, palette='viridis')
plt.title('Jumlah Penjualan Berdasarkan Hari dalam Seminggu', fontsize=16)
plt.xlabel('Hari', fontsize=14)
plt.ylabel('Jumlah Penjualan (cnt)', fontsize=14)
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Pertanyaan 2: Hubungan antara Temperatur dan Jumlah Penjualan
st.subheader("2. Apa hubungan antara faktor cuaca harian (seperti temperatur) dan jumlah penjualan harian?")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=day_df, x='temp', y='cnt')
plt.title('Hubungan antara Temperatur dan Jumlah Penjualan', fontsize=16)
plt.xlabel('Temperatur (°C)', fontsize=14)
plt.ylabel('Jumlah Penjualan (cnt)', fontsize=14)
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Menghitung koefisien regresi (slope) dan intercept secara manual
X = day_df['temp']
y = day_df['cnt']

n = len(X)
x_mean = X.mean()
y_mean = y.mean()

# Menghitung slope (b1) dan intercept (b0)
numerator = ((X - x_mean) * (y - y_mean)).sum()
denominator = ((X - x_mean) ** 2).sum()

slope = numerator / denominator
intercept = y_mean - slope * x_mean

# Memprediksi nilai
y_pred = intercept + slope * X

# Visualisasi dengan garis regresi
plt.figure(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=day_df)
plt.plot(X, y_pred, color='orange', linewidth=2, label='Garis Regresi')
plt.title('Jumlah Penjualan vs Suhu dengan Garis Regresi', fontsize=16)
plt.xlabel('Suhu (°C)', fontsize=14)
plt.ylabel('Jumlah Penjualan', fontsize=14)
plt.legend()
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Menampilkan hasil koefisien
st.subheader("Hasil Koefisien Regresi")
st.write(f'Koefisien (slope): {slope}')
st.write(f'Intercept: {intercept}')

# Hasil Clustering K-Means Manual
st.subheader("Hasil Clustering K-Means Manual")
k = 2  # Mengatur jumlah cluster menjadi 2

# Inisialisasi centroid secara acak
centroids = day_df[['temp', 'cnt']].sample(n=k).values
max_iterations = 100

# Proses K-Means
for _ in range(max_iterations):
    # Hitung jarak dari setiap titik ke centroid
    distances = np.linalg.norm(day_df[['temp', 'cnt']].values[:, np.newaxis] - centroids, axis=2)
    
    # Tentukan cluster untuk setiap titik
    clusters = np.argmin(distances, axis=1)
    
    # Hitung centroid baru
    new_centroids = np.array([day_df[['temp', 'cnt']].values[clusters == i].mean(axis=0) for i in range(k)])
    
    # Jika centroid tidak berubah, keluar dari loop
    if np.all(centroids == new_centroids):
        break
    
    centroids = new_centroids

# Tambahkan cluster ke DataFrame
day_df['cluster'] = clusters

# Visualisasi hasil clustering
plt.figure(figsize=(10, 6))
for i in range(k):
    plt.scatter(day_df.loc[day_df['cluster'] == i, 'temp'],
                day_df.loc[day_df['cluster'] == i, 'cnt'],
                label=f'Cluster {i}')
    
plt.scatter(centroids[:, 0], centroids[:, 1], color='red', marker='x', s=200, label='Centroids')
plt.title('Hasil Clustering K-Means Manual', fontsize=16)
plt.xlabel('Temperatur (°C)')
plt.ylabel('Jumlah Penjualan (cnt)')
plt.legend()
st.pyplot(plt)
plt.clf()

# Visualisasi Korelasi
st.subheader("Korelasi Antara Fitur")
numerical_cols = day_df.select_dtypes(include=['number']).columns
corr = day_df[numerical_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Korelasi antara Fitur', fontsize=16)
st.pyplot(plt)
plt.clf()

# Temuan Utama
st.subheader("Temuan Utama")
st.write("1. Penjualan menunjukkan pola yang jelas sepanjang minggu, dengan penjualan lebih tinggi pada akhir pekan.")
st.write("2. Terdapat korelasi positif antara temperatur dan penjualan, menunjukkan bahwa cuaca yang lebih hangat meningkatkan penggunaan sepeda.")

# Hak cipta
st.caption('Copyright © Zidan Alfariza Putra Pratama 2024')
