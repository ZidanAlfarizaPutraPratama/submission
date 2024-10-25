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

# Mengubah kolom 'dteday' ke format datetime
dataframes['day']['date'] = pd.to_datetime(dataframes['day']['dteday'])

# Menilai DataFrame day
st.subheader("Menilai DataFrame Harian:")
st.write("Informasi DataFrame Harian:")
st.text(dataframes['day'].info())
st.write("Jumlah nilai yang hilang:")
st.write(dataframes['day'].isna().sum())
st.write("Jumlah duplikasi:", dataframes['day'].duplicated().sum())
st.write("Statistik deskriptif:")
st.write(dataframes['day'].describe())

# Filter berdasarkan tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", value=dataframes['day']['date'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", value=dataframes['day']['date'].max())

# Filter berdasarkan musim
seasons = dataframes['day']['season'].unique()
selected_season = st.sidebar.multiselect("Pilih Musim", seasons, default=seasons)

# Filter DataFrame berdasarkan tanggal dan musim
filtered_data = dataframes['day'][
    (dataframes['day']['date'] >= pd.to_datetime(start_date)) & 
    (dataframes['day']['date'] <= pd.to_datetime(end_date)) &
    (dataframes['day']['season'].isin(selected_season))
]

if not filtered_data.empty:
    st.title("Dashboard Data Penjualan")

    # Menampilkan statistik deskriptif
    st.write("Statistik Deskriptif untuk Data yang Dipilih:")
    st.write(filtered_data.describe())

    # EDA Univariate: Distribusi penjualan harian
    plt.figure(figsize=(12, 6))
    sns.histplot(filtered_data['cnt'], bins=30, kde=True)
    plt.title('Distribusi Jumlah Penjualan Harian')
    plt.xlabel('Jumlah Penjualan (cnt)')
    plt.ylabel('Frekuensi')
    st.pyplot(plt)
    plt.clf()

    # EDA Kategorikal: Rata-rata penjualan per musim
    plt.figure(figsize=(12, 6))
    sns.barplot(x='season', y='cnt', data=filtered_data, ci=None)
    plt.title('Rata-rata Penjualan Per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata Jumlah Penjualan (cnt)')
    st.pyplot(plt)
    plt.clf()

    # EDA: Penjualan berdasarkan kondisi cuaca
    plt.figure(figsize=(12, 6))
    sns.barplot(x='weathersit', y='cnt', data=filtered_data, ci=None)
    plt.title('Rata-rata Penjualan Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Jumlah Penjualan (cnt)')
    st.pyplot(plt)
    plt.clf()

    # EDA Multivariate: Heatmap korelasi
    plt.figure(figsize=(10, 8))
    numeric_cols = filtered_data.select_dtypes(include=['number']).columns
    corr = filtered_data[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Korelasi antara Fitur')
    st.pyplot(plt)
    plt.clf()

    # EDA Numerikal: Scatter plot
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='temp', y='cnt', data=filtered_data)
    plt.title('Scatter Plot Temp vs Jumlah Penjualan')
    plt.xlabel('Temperatur')
    plt.ylabel('Jumlah Penjualan (cnt)')
    st.pyplot(plt)
    plt.clf()

    # Cek DataFrame hour
    if not dataframes['hour'].empty:
        st.subheader("Analisis Data Penjualan Per Jam")

        # Jumlah penjualan per jam
        sales_per_hour = dataframes['hour'].groupby('hr')['cnt'].sum().reset_index()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x='hr', y='cnt', data=sales_per_hour)
        plt.title('Jumlah Penjualan Per Jam')
        plt.xlabel('Jam')
        plt.ylabel('Jumlah Penjualan (cnt)')
        st.pyplot(plt)
        plt.clf()
    else:
        st.warning("Data per jam kosong.")
else:
    st.warning("Data harian kosong.")

# Menambahkan copyright
st.caption('Copyright © Zidan Alfariza Putra Pratama 2024')
