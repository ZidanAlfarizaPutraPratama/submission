import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set gaya seaborn dan palet warna
sns.set(style='darkgrid', palette='muted')

# URL dataset
DATA_URLS = {
    "day": "https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/day.csv",
    "hour": "https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/hour.csv",
}

# Fungsi untuk memuat dataset
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

# Menilai DataFrame Harian
st.subheader("Menilai DataFrame Harian:")
st.write("Informasi DataFrame Harian:")
st.text(dataframes['day'].info())
st.write("Jumlah nilai yang hilang:")
st.write(dataframes['day'].isna().sum())
st.write("Jumlah duplikasi:", dataframes['day'].duplicated().sum())
st.write("Statistik deskriptif:")
st.write(dataframes['day'].describe())

# Filter data
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", value=dataframes['day']['date'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", value=dataframes['day']['date'].max())
seasons = dataframes['day']['season'].unique()
selected_season = st.sidebar.multiselect("Pilih Musim", seasons, default=seasons)

# Filter DataFrame
filtered_data = dataframes['day'][
    (dataframes['day']['date'] >= pd.to_datetime(start_date)) & 
    (dataframes['day']['date'] <= pd.to_datetime(end_date)) &
    (dataframes['day']['season'].isin(selected_season))
]

# Tampilkan kolom data yang sudah difilter
st.write("Kolom dalam DataFrame yang difilter:", filtered_data.columns)

if not filtered_data.empty:
    st.title("Dashboard Data Penjualan")

    # Statistik deskriptif untuk data yang difilter
    st.write("Statistik Deskriptif untuk Data yang Dipilih:")
    st.write(filtered_data.describe())

    # Analisis Univariate: Distribusi penjualan harian
    plt.figure(figsize=(12, 6))
    sns.histplot(filtered_data['cnt'], bins=30, kde=True, color='skyblue')
    plt.title('Distribusi Jumlah Penjualan Harian', fontsize=16)
    plt.xlabel('Jumlah Penjualan (cnt)', fontsize=14)
    plt.ylabel('Frekuensi', fontsize=14)
    st.pyplot(plt)
    plt.clf()

    # Visualisasi rata-rata penjualan
    average_sales = filtered_data['cnt'].mean()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=['Rata-rata Penjualan'], y=[average_sales], color='coral')
    plt.title('Rata-rata Jumlah Penjualan Harian', fontsize=16)
    plt.xlabel('Keterangan', fontsize=14)
    plt.ylabel('Rata-rata Jumlah Penjualan (cnt)', fontsize=14)
    st.pyplot(plt)
    plt.clf()

    # Heatmap korelasi
    plt.figure(figsize=(10, 8))
    numerical_cols = filtered_data.select_dtypes(include=['number']).columns
    corr = filtered_data[numerical_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=.5)
    plt.title('Korelasi antara Fitur', fontsize=16)
    st.pyplot(plt)
    plt.clf()

    # Scatter plot untuk temperatur vs penjualan
    if 'temp' in filtered_data.columns: 
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=filtered_data, x='temp', y='cnt', color='mediumseagreen', alpha=0.7)
        plt.title('Scatter Plot Temperatur vs Jumlah Penjualan', fontsize=16)
        plt.xlabel('Temperatur', fontsize=14)
        plt.ylabel('Jumlah Penjualan (cnt)', fontsize=14)
        st.pyplot(plt)
        plt.clf()
    else:
        st.warning("Kolom 'temp' tidak ditemukan dalam data yang difilter.")

    # Analisis RFM
    st.subheader("Analisis RFM")

    rfm_data = filtered_data.groupby('instant').agg({
        'date': 'max',
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).rename(columns={'date': 'Recency', 'cnt': 'Monetary'})

    rfm_data['Recency'] = (filtered_data['date'].max() - rfm_data['Recency']).dt.days
    rfm_data['Frequency'] = rfm_data['casual'] + rfm_data['registered']

    st.write("Data RFM:")
    st.write(rfm_data[['Recency', 'Monetary', 'Frequency']])

    # Binning untuk Frequency
    rfm_data['Frequency_Bin'] = pd.cut(rfm_data['Frequency'], bins=[0, 1, 5, 10, 20, 100], 
                                        labels=['1', '2-5', '6-10', '11-20', '20+'])

    st.write("Data RFM setelah Binning:")
    st.write(rfm_data[['Recency', 'Monetary', 'Frequency', 'Frequency_Bin']])

    # Clustering Manual
    st.subheader("Clustering Manual")
    rfm_data['Monetary_Bin'] = pd.cut(rfm_data['Monetary'], bins=[0, 100, 200, 500, 1000, float('inf')], 
                                       labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

    st.write("Hasil Clustering Manual berdasarkan Monetary:")
    st.write(rfm_data[['Monetary', 'Monetary_Bin']])

    # Analisis penjualan per jam
    if not dataframes['hour'].empty:
        st.subheader("Analisis Data Penjualan Per Jam")
        sales_per_hour = dataframes['hour'].groupby('hr')['cnt'].sum().reset_index()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x='hr', y='cnt', data=sales_per_hour, palette='muted')
        plt.title('Jumlah Penjualan Per Jam', fontsize=16)
        plt.xlabel('Jam', fontsize=14)
        plt.ylabel('Jumlah Penjualan (cnt)', fontsize=14)
        st.pyplot(plt)
        plt.clf()
    else:
        st.warning("Data per jam kosong.")
else:
    st.warning("Data harian kosong.")

# Hak cipta
st.caption('Copyright © Zidan Alfariza Putra Pratama 2024')
