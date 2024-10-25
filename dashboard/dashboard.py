import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set gaya seaborn
sns.set(style='dark')

# Tentukan direktori data
DATA_DIR = r"D:\Submission\data\\"

# Fungsi untuk memuat dataset dengan penanganan kesalahan
def load_data(file_name):
    full_path = os.path.join(DATA_DIR, file_name)
    try:
        return pd.read_csv(full_path)
    except FileNotFoundError:
        st.error(f"File {full_path} tidak ditemukan.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error(f"File {full_path} kosong.")
        return pd.DataFrame()

# Memuat dataset
datasets = {
    "day": "day.csv",
    "hour": "hour.csv",
}

dataframes = {name: load_data(file) for name, file in datasets.items()}

# Memeriksa kolom yang ada di kedua DataFrame
if 'instant' in dataframes['day'].columns and 'instant' in dataframes['hour'].columns:
    merged_df = pd.merge(dataframes['day'], dataframes['hour'], on='instant', how='left')
else:
    st.error("Kolom 'instant' tidak ditemukan di salah satu DataFrame.")

# Lanjutkan dengan analisis data jika merged_df tidak kosong
if not merged_df.empty:
    st.title("Dashboard Data")

    # Tampilkan data yang digabungkan
    st.write("Data yang digabungkan:", merged_df)

    # Visualisasi total penjualan per jam
    if 'cnt' in merged_df.columns:
        sales_per_hour = merged_df.groupby('hr')['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='hr', y='cnt', data=sales_per_hour, ax=ax, palette='Blues_d')
        ax.set_title("Total Penjualan per Jam")
        st.pyplot(fig)

else:
    st.warning("Data yang digabungkan kosong.")
