```markdown
# Dicoding Collection Dashboard ✨

## Setup Environment - Anaconda
Untuk menggunakan Anaconda, jalankan perintah berikut:

```bash
conda create --name main-ds python
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
Jika menggunakan shell/terminal biasa, ikuti langkah-langkah ini:

```bash
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Menjalankan Aplikasi Streamlit
Setelah lingkungan disiapkan, jalankan perintah berikut untuk memulai aplikasi:

```bash
streamlit run dashboard.py
```

## Struktur File
- `dashboard.py`: Kode sumber utama aplikasi dashboard.
- Data diambil dari URL berikut:
  - [day.csv](https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/day.csv)
  - [hour.csv](https://raw.githubusercontent.com/ZidanAlfarizaPutraPratama/submission/master/data/hour.csv)

## Copyright
Copyright © Dicoding 2023 | Zidan Alfariza Putra Pratama 2024
```
