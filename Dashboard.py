import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('https://github.com/indrriikkk/Analysis-Bike-Sharing/blob/a9392edd5f213fe156a2693dc1a2b54383352b36/hour.csv')

# Title
st.title('Analisis Penyewaan Sepeda')

# About me
st.markdown("""
- **Nama**: Indri Syafitri
- **Email**: indrisyafitri78@gmail.com
- **Dicoding ID**: indri_syafitri
""")

# Sidebar
with st.sidebar:
    st.image("https://github.com/indrriikkk/Analysis-Bike-Sharing/blob/fe494fbef095c542d1ab1fe69a9de5473cbca939/bike-share.png")

    df.sort_values(by="date", inplace=True)
    df.reset_index(inplace=True)

    df["date"] = pd.to_datetime(df["date"])

    min_date = df["date"].min()
    max_date = df["date"].max()

    # Membuat filter rentang tanggal
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu', min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

    # Mengolah data sesuai rentang tanggal yang diinput
    df_filtered = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]


# Set style seaborn
sns.set(style='dark')

df = pd.read_csv('https://github.com/indrriikkk/Analysis-Bike-Sharing/blob/fe494fbef095c542d1ab1fe69a9de5473cbca939/hour.csv')

# Mengubah nama judul kolom
df.rename(columns={'dteday': 'date', 'yr': 'year', 'mnth': 'month', 'hr': 'hour',
                   'weathersit': 'weather', 'casual': 'casual_user', 'registered': 'registered_user',
                   'hum': 'humidity', 'cnt': 'count', 'atemp': 'apparent_temp'},
          inplace=True)

# Mengubah angka menjadi keterangan
df.loc[df['holiday'] == 0, 'holiday'] = 'No'
df.loc[df['holiday'] == 1, 'holiday'] = 'Yes'

df.loc[df['season'] == 1, 'season'] = 'Winter'
df.loc[df['season'] == 2, 'season'] = 'Spring'
df.loc[df['season'] == 3, 'season'] = 'Summer'
df.loc[df['season'] == 4, 'season'] = 'Fall'

df.loc[df['workingday'] == 0, 'workingday'] = 'No'
df.loc[df['workingday'] == 1, 'workingday'] = 'Yes'

df.loc[df['weekday'] == 0, 'weekday'] = 'Monday'
df.loc[df['weekday'] == 1, 'weekday'] = 'Tuesday'
df.loc[df['weekday'] == 2, 'weekday'] = 'Wednesday'
df.loc[df['weekday'] == 3, 'weekday'] = 'Thursday'
df.loc[df['weekday'] == 4, 'weekday'] = 'Friday'
df.loc[df['weekday'] == 5, 'weekday'] = 'Saturday'
df.loc[df['weekday'] == 6, 'weekday'] = 'Sunday'

df.loc[df['month'] == 1, 'month'] = 'January'
df.loc[df['month'] == 2, 'month'] = 'February'
df.loc[df['month'] == 3, 'month'] = 'March'
df.loc[df['month'] == 4, 'month'] = 'April'
df.loc[df['month'] == 5, 'month'] = 'May'
df.loc[df['month'] == 6, 'month'] = 'June'
df.loc[df['month'] == 7, 'month'] = 'July'
df.loc[df['month'] == 8, 'month'] = 'August'
df.loc[df['month'] == 9, 'month'] = 'September'
df.loc[df['month'] == 10, 'month'] = 'October'
df.loc[df['month'] == 11, 'month'] = 'November'
df.loc[df['month'] == 12, 'month'] = 'December'

df.loc[df['year'] == 0, 'year'] = '2011'
df.loc[df['year'] == 1, 'year'] = '2012'

df.loc[df['weather'] == 1, 'weather'] = 'Clear'
df.loc[df['weather'] == 2, 'weather'] = 'Mist-Cloudy'
df.loc[df['weather'] == 3, 'weather'] = 'Light-Rain'
df.loc[df['weather'] == 4, 'weather'] = 'Heavy-Rain'


# Parameter Statistik Deskriptif
st.subheader('Parameter Statistik Deskriptif')
st.write(df.describe())

# membuat heatmap untuk memvisualisasikan matriks korelasi kolom numerik
st.subheader('Heatmap')
fig, ax = plt.subplots(figsize=(10, 5))
correlation_matrix = df.corr(numeric_only=True)
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

sns.heatmap(
    correlation_matrix,
    annot=True,
    mask=mask,
    cmap="inferno",
    center=0,
    fmt=".2f",
)
ax.set_title("Correlation Heatmap")
st.pyplot(plt)

# Membuat jumlah penyewaan berdasarkan bulan dan jam dalam jumlah sewa sepeda harian
st.subheader('Pola Jumlah Sewa Sepeda Harian Berdasarkan Jam')

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(x="hour", y="count", data=df, ci=None)
plt.title("Pola Jumlah Sewa Sepeda Harian Berdasarkan Jam")
plt.xlabel("Jam")
plt.ylabel("Jumlah Sewa Sepeda Harian")
st.pyplot(plt)

# Membuat perbandingan penyewaan saat musim semi dengan musim lainnya
st.subheader('Rental Permusim')

season_df = df.groupby('season')['count'].mean()
season_names = ['Spring', 'Summer', 'Fall', 'Winter']
plt.figure()  # Tambahkan ini untuk membuat gambar baru sebelum plot kedua
plt.bar(season_names, season_df)
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Sewa Berdasarkan Jam')
plt.title('Dampak Tiap Musim Terhadap Jumlah Penyewaan Sepeda Berdasarkan Jam')
st.pyplot(plt)

# Kesimpulan
st.subheader('Kesimpulan')
st.write("""
- Dapat dilihat dari diagram batang yang ditampilkan, musim dengan jumlah penyewa sepeda paling banyak adalah musim gugur dan musim dengan jumlah penyewa paling sedikit adalah musim salju. Musim Panas berada pada urutan kedua terbanyak penyewa. Kesimpulannya, pada musim panas mengalami peningkatan penyewaan namun, jika dibandingkan dengan musim gugur, musim gugur menjadi urutan terbanyak dan diikuti musim panas di urutan kedua.
- Berdasarkan line plot yang ditampilkan, dapat ditarik kesimpulan bahwa ada pola jam ketika penyewa sepeda meningkat, yaitu sekitar di jam 8 pagi dan sekitar jam 5 atau 6 sore
""")

st.caption('Copyright (c) Indri Syafitri')