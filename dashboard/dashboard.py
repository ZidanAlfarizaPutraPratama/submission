import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set gaya seaborn
sns.set(style='dark')

# URL dataset dari GitHub
DATA_URLS = {
    "day": "https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/day.csv",
    "hour": "https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/hour.csv",
}

# Fungsi untuk memuat dataset dengan penanganan kesalahan
def load_data(url):
    try:
        return pd.read_csv(url)
    except pd.errors.EmptyDataError:
        st.error("File kosong.")
        return pd.DataFrame()

# Memuat dataset
dataframes = {name: load_data(url) for name, url in DATA_URLS.items()}

# Menilai DataFrame day
st.subheader("Menilai DataFrame Harian:")
st.write("Informasi DataFrame Harian:")
st.text(dataframes['day'].info())
st.write("Jumlah nilai yang hilang:")
st.write(dataframes['day'].isna().sum())
st.write("Jumlah duplikasi:", dataframes['day'].duplicated().sum())
st.write("Statistik deskriptif:")
st.write(dataframes['day'].describe())

# Menilai DataFrame hour
st.subheader("Menilai DataFrame Jam:")
st.write("Informasi DataFrame Jam:")
st.text(dataframes['hour'].info())
st.write("Jumlah nilai yang hilang:")
st.write(dataframes['hour'].isna().sum())
st.write("Jumlah duplikasi:", dataframes['hour'].duplicated().sum())
st.write("Statistik deskriptif:")
st.write(dataframes['hour'].describe())

# Cek apakah kolom 'date' ada di day_df
if 'date' in dataframes['day'].columns:
    sales_per_day = dataframes['day'].groupby('date')['cnt'].sum().reset_index()
else:
    st.write("Kolom 'date' tidak ditemukan di day_df. Berikut adalah kolom yang ada:")
    st.write(dataframes['day'].columns)

# Lanjutkan dengan analisis data jika day_df tidak kosong
if not dataframes['day'].empty:
    st.title("Dashboard Data Penjualan")

    # Visualisasi distribusi jumlah penjualan harian
    plt.figure(figsize=(12, 6))
    sns.histplot(dataframes['day']['cnt'], bins=30, kde=True)
    plt.title('Distribusi Jumlah Penjualan Harian')
    plt.xlabel('Jumlah Penjualan (cnt)')
    plt.ylabel('Frekuensi')
    st.pyplot(plt)
    plt.clf()  # Membersihkan plot

    # Jumlah penjualan per jam
    if not dataframes['hour'].empty:
        sales_per_hour = dataframes['hour'].groupby('hr')['cnt'].sum().reset_index()

        plt.figure(figsize=(12, 6))
        sns.barplot(x='hr', y='cnt', data=sales_per_hour)
        plt.title('Jumlah Penjualan Per Jam')
        plt.xlabel('Jam')
        plt.ylabel('Jumlah Penjualan (cnt)')
        st.pyplot(plt)
        plt.clf()  # Membersihkan plot
    else:
        st.warning("Data per jam kosong.")
else:
    st.warning("Data harian kosong.")

# Menambahkan copyright
st.caption('Copyright © Zidan Alfariza Putra Pratama 2024')
