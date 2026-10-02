# Proyek Analisis Data: Bike Sharing Dataset (Capital Bikeshare) 🚲

Analisis penyewaan sepeda sistem Capital Bikeshare (Washington D.C.) per jam dan per hari, 1 Januari 2011 – 31 Desember 2012, lengkap dengan notebook analisis dan dashboard interaktif Streamlit.

## Pertanyaan Bisnis
1. Pada pukul berapa rata-rata penyewaan per jam mencapai puncak pada hari kerja dibandingkan akhir pekan/hari libur, dan berapa persen penyewa pada jam puncak tersebut adalah pengguna *registered*?
2. Berapa persen rata-rata penyewaan harian turun saat cuaca berkabut/mendung dan hujan/salju ringan dibanding cuaca cerah, dan musim apa yang memiliki penyewaan harian tertinggi dan terendah?
3. Berapa persen pertumbuhan total penyewaan dari 2011 ke 2012 (*year-over-year*), bulan apa yang tumbuh paling tinggi dan paling rendah, dan bagaimana perubahan porsi pengguna *casual*?

Analisis lanjutan (tanpa *machine learning*): ***manual grouping/binning*** (segmen waktu, bin suhu 5°C, dan tier permintaan harian).

## Struktur Direktori
```
submission_bike_sharing
├── dashboard
│   ├── dashboard.py        # aplikasi Streamlit
│   └── main_data.csv       # data per jam yang sudah bersih (hasil notebook)
├── data
│   ├── day.csv             # data harian asli
│   └── hour.csv            # data per jam asli
├── .streamlit
│   └── config.toml         # tema dashboard
├── notebook.ipynb          # proses analisis lengkap (sudah dijalankan)
├── README.md
├── requirements.txt
└── url.txt                 # tautan dashboard di Streamlit Community Cloud
```

## Setup Environment

### Anaconda
```
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

### Shell/Terminal
```
cd submission_bike_sharing
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Menjalankan Dashboard
Jalankan dari folder utama proyek (`submission_bike_sharing`, yang berisi `requirements.txt`):
```
streamlit run dashboard/dashboard.py
```
Dashboard terbuka di `http://localhost:8501`. Gunakan panel filter (rentang tanggal, musim, cuaca) di sebelah kiri; tiap tab menjawab satu pertanyaan bisnis, ditambah tab analisis lanjutan.

## Menjalankan Notebook
Buka `notebook.ipynb` dengan Jupyter (`pip install jupyter`), VS Code, atau Google Colab (unggah folder `data` bersama notebook), lalu pilih *Run All*. Jalankan dari folder utama proyek (`submission_bike_sharing`) agar jalur `data/` terbaca. Menjalankan notebook akan memperbarui `dashboard/main_data.csv`.

## Deploy ke Streamlit Community Cloud
1. Unggah isi folder `submission_bike_sharing` ke repositori GitHub publik:
```
git init
git add .
git commit -m "Proyek analisis data"
git branch -M main
git remote add origin https://github.com/<username>/<nama-repo>.git
git push -u origin main
```
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan GitHub, klik **Create app**, pilih repositori dan *branch* `main`, isi **Main file path** dengan `dashboard/dashboard.py`.
3. Klik **Deploy**, lalu salin URL aplikasi ke `url.txt`.

## Sumber Data
Bike Sharing Dataset (Fanaee-T & Gama, UCI Machine Learning Repository), data Capital Bikeshare Washington D.C. 2011–2012: `day.csv` (731 hari) dan `hour.csv` (17.379 jam). Pada dataset asli label `season` tertukar (Januari tercatat sebagai *spring*); notebook memetakannya ulang berdasarkan bulan dan suhu.
