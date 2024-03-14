import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv(r"dasboard/mixel.csv")
day_df.head()

drop_col = ['windspeed']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama judul kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df


# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

image_url = 'https://upload.wikimedia.org/wikipedia/commons/9/97/Sepeda_Onthel.jpg'
with st.sidebar:
    st.image(image_url, caption='bike', use_column_width=True)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Rental Dashboard 🚲')

def custom_format(number):
    parts = f"{number:,}".split(",")
    if len(parts) > 1:
        return f"{parts[0]}, {','.join(parts[1:])}"
    return f"{number}"

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value=custom_format(daily_rent_casual))
    st.markdown("---")

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value=custom_format(daily_rent_registered))
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value=custom_format(daily_rent_total))

st.markdown("""
      ### Perbedaan Pengguna Casual  dan Pengguna Terdaftar:
      
      #### Pengguna Casual :
      
      - Proses sewa yang lebih simpel: Biasanya pengguna casual dapat menyewa sepeda tanpa perlu membuat akun atau melalui proses pendaftaran yang rumit.
      - Opsi pembayaran yang lebih terbatas: Pengguna casual mungkin hanya bisa menggunakan metode pembayaran tertentu, seperti kartu kredit atau debit tanpa kontak, untuk menyewa sepeda.
      - Akses fitur terbatas: Pengguna casual mungkin tidak memiliki akses ke semua fitur yang tersedia dalam aplikasi atau layanan penyewaan sepeda, seperti riwayat sewa, poin reward, atau opsi untuk memperpanjang sewa.
      - Biaya sewa yang lebih tinggi: Dalam beberapa penyewaan sepeda, pengguna casual mungkin dikenakan biaya sewa yang lebih tinggi dibandingkan pengguna terdaftar.
      
      #### Pengguna Terdaftar:
      
      - Memiliki akun: Pengguna terdaftar telah membuat akun pada aplikasi atau layanan penyewaan sepeda.
      - Proses sewa yang lebih efisien: Dengan akun terdaftar, proses sewa sepeda biasanya menjadi lebih efisien karena informasi pengguna sudah tersimpan.
      - Akses ke semua fitur: Pengguna terdaftar biasanya memiliki akses ke semua fitur yang ditawarkan oleh aplikasi atau layanan penyewaan sepeda.
      - Potensi biaya sewa yang lebih rendah: Pengguna terdaftar mungkin bisa mendapatkan potongan harga, reward, atau paket sewa khusus yang lebih hemat dibandingkan pengguna casual.
      - Kemungkinan opsi pembayaran yang lebih beragam: Selain metode pembayaran umum, pengguna terdaftar mungkin bisa menggunakan opsi lain seperti dompet digital atau voucher khusus.
      """, unsafe_allow_html=True)

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
def with_juta(x, pos):
    # Assuming 'count' is in the thousands ('000). For actual values in 'jt', adjust accordingly.
    return '{:1.1f} jt'.format(x * 1e-3)

formatter = FuncFormatter(with_juta)

# Create the dataframe for plotting
monthly_rent_df = create_monthly_rent_df(day_df)  # Replace 'day_df' with your actual dataframe

fig, ax = plt.subplots(figsize=(24, 8))

# Plot the data
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o', 
    markersize=10,
    linewidth=3,
    linestyle='-',
    color='tab:blue'
)

# Annotate data points with formatted labels
for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row, with_juta(row, None), ha='center', va='bottom', fontsize=13, fontweight='bold', color='darkblue')

# Set major formatter for y-axis
ax.yaxis.set_major_formatter(formatter)

# Improve the aesthetics
ax.set_title('Monthly Bike Rentals', fontsize=26, fontweight='bold', pad=20)
ax.set_xlabel('Month', fontsize=20, labelpad=15)
ax.set_ylabel('Number of Rentals', fontsize=20, labelpad=15)
ax.tick_params(axis='x', labelsize=20, rotation=45)
ax.tick_params(axis='y', labelsize=20)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_facecolor('whitesmoke')  # Set a background color

# Add a legend
ax.legend(['Total Rentals'], fontsize=14, frameon=True, shadow=True)

# Tight layout to ensure nothing is clipped
plt.tight_layout()

# Show the plot
st.pyplot(fig)

st.markdown('''

### Analisis:

Musim panas (Juni-Agustus) adalah periode dengan permintaan sewa sepeda tertinggi. Hal ini kemungkinan disebabkan oleh cuaca yang hangat dan cerah, yang mendorong orang untuk lebih banyak beraktivitas di luar ruangan.

Musim dingin (Desember-Februari) adalah periode dengan permintaan sewa sepeda terendah. Hal ini kemungkinan disebabkan oleh cuaca yang dingin dan bersalju, yang membuat orang enggan untuk bersepeda.

Ada sedikit peningkatan permintaan sewa sepeda di musim semi (Maret-Mei) dan musim gugur (September-November). Hal ini kemungkinan disebabkan oleh cuaca yang lebih moderat, yang membuat orang lebih nyaman untuk bersepeda.

### Kesimpulan:

Tren musiman yang jelas dalam penyewaan sepeda menunjukkan bahwa permintaan untuk layanan ini sangat dipengaruhi oleh cuaca. Perusahaan penyewaan sepeda dapat menggunakan data ini untuk merencanakan strategi bisnis mereka dan memastikan bahwa mereka memiliki persediaan sepeda yang memadai untuk memenuhi permintaan.
''')


# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonly Rentals')

def with_units(x, pos):
    """The two args are the value and tick position."""
    if x >= 1e6:  # If the value is in the millions
        return '{:1.1f} jt'.format(x*1e-6)
    return '{:1.0f} jt'.format(x*1e-3)  # Value is in the thousands

formatter = FuncFormatter(with_units)

fig, ax = plt.subplots(figsize=(16, 8))

# Create a new melted dataframe for the seaborn barplot
melted_season_rent_df = season_rent_df.melt(id_vars='season', value_vars=['registered', 'casual'],
                                            var_name='type', value_name='count')

# Create the barplot with seaborn
sns.barplot(x='season', y='count', hue='type', data=melted_season_rent_df, ax=ax)

# Set custom formatting for y-axis labels
ax.yaxis.set_major_formatter(formatter)

# Place the barplot labels
for p in ax.patches:
    # You'll want to format this with the same logic as your y-axis labels
    label = with_units(p.get_height(), None)
    ax.annotate(label, 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', xytext=(0, 10), 
                textcoords='offset points')

# Set the labels and ticks
ax.set_xlabel('Season', fontsize=15)
ax.set_ylabel('Number of Rentals', fontsize=15)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.legend(title='Type')

# Display the plot
st.pyplot(fig)
st.markdown('''
## Analisis:

### Tren Musiman:

Di America, terdapat tren musiman yang menarik dalam persewaan musiman, yang mungkin mengindikasikan perubahan pola pariwisata atau aktivitas rekreasi.

Secara keseluruhan, Musim Gugur tampaknya menjadi musim paling populer untuk persewaan, dengan jumlah penyewa terdaftar dan penyewa biasa terbanyak. Hal ini mungkin disebabkan oleh beberapa faktor, seperti kondisi cuaca yang menyenangkan dan mendukung aktivitas luar ruangan, atau dedaunan musim gugur yang menarik wisatawan ke wilayah tertentu.

Musim semi mengikuti musim gugur dalam hal total sewa, dengan distribusi serupa antara penyewa terdaftar dan penyewa biasa. Hal ini menunjukkan bahwa Musim Semi juga merupakan waktu yang populer bagi orang-orang untuk menikmati aktivitas luar ruangan dengan bersepeda.

Musim panas tampaknya menjadi musim yang paling tidak populer untuk persewaan, dengan jumlah penyewa terendah secara keseluruhan. Mungkin ada beberapa alasan untuk hal ini. Kondisi cuaca yang panas mungkin membuat bersepeda menjadi kurang menarik bagi sebagian orang. Selain itu, musim panas mungkin merupakan waktu ketika orang lebih cenderung melakukan perjalanan ke tempat-tempat yang tidak menggunakan sepeda sebagai moda transportasi utama.

Sewa musim dingin sedikit lebih tinggi daripada sewa musim panas. Hal ini mungkin disebabkan oleh orang-orang yang menggunakan sepeda untuk bepergian atau melakukan keperluan lain selama bulan-bulan musim dingin, terutama di daerah dengan cuaca musim dingin yang sejuk.

Penting untuk dicatat bahwa data ini hanya mencerminkan jumlah penyewa dan tidak memberi tahu kami jangka waktu sewa mereka. Jadi, meskipun Musim Gugur memiliki penyewa terbanyak, kami tidak tahu apakah mereka menyewa untuk perjalanan singkat atau perjalanan yang lebih lama.

Analisis data lebih lanjut yang menggabungkan durasi sewa dan variasi musiman dapat memberikan gambaran pola sewa yang lebih komprehensif.
.
''')

##Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f'{num:.1f}{" kMGTPE"[magnitude]}'.strip()

# Custom palette
palette = sns.color_palette("coolwarm", 7)

st.subheader('Weekday, Workingday, and Holiday Rentals')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 15), sharex=False)

# Set up a formatter for the y-axis
formatter = FuncFormatter(human_format)

## Plot for rentals based on working day
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette=palette[:2],
    ax=axes[0])
axes[0].yaxis.set_major_formatter(formatter)
axes[0].set_title('Number of Rentals based on Working Day', fontsize=18)
axes[0].set_xlabel('Working Day (0 = No, 1 = Yes)', fontsize=14)
axes[0].set_ylabel('Number of Rentals', fontsize=14)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=12)

## Plot for rentals based on holiday
sns.barplot(
    x='holiday',
    y='count',
    data=holiday_rent_df,
    palette=palette[:2],
    ax=axes[1])
axes[1].yaxis.set_major_formatter(formatter)
axes[1].set_title('Number of Rentals based on Holiday', fontsize=18)
axes[1].set_xlabel('Holiday (0 = No, 1 = Yes)', fontsize=14)
axes[1].set_ylabel('Number of Rentals', fontsize=14)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=12)

## Plot for rentals based on a weekday
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=palette,
    ax=axes[2])
axes[2].yaxis.set_major_formatter(formatter)
axes[2].set_title('Number of Rentals based on Weekday', fontsize=18)
axes[2].set_xticklabels(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], fontsize=13)
axes[2].set_xlabel('Day of the Week', fontsize=14)
axes[2].set_ylabel('Number of Rentals', fontsize=14)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=12)

# Add human-readable labels on top of the bars
for i, ax in enumerate(axes):
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), human_format(p.get_height(), None), 
                fontsize=11, color='black', ha='center', va='bottom')

plt.tight_layout()
st.pyplot(fig)

st.markdown("""
### Analisis Perbedaan Penyewaan Sepeda pada Hari Kerja, Akhir Pekan, dan Hari Libur:

Data menunjukkan bahwa terdapat perbedaan signifikan dalam jumlah penyewaan sepeda pada hari kerja, akhir pekan, dan hari libur.

#### Hari Kerja:

Hari kerja memiliki jumlah penyewaan tertinggi, menunjukkan bahwa banyak orang menggunakan sepeda sebagai alat transportasi untuk pergi bekerja. Hal ini dapat disebabkan oleh beberapa faktor:

- **Meningkatnya Kesadaran akan Kesehatan:** Orang-orang semakin sadar akan manfaat kesehatan dari bersepeda dan memilihnya sebagai alternatif yang lebih sehat daripada kendaraan pribadi.
- **Biaya yang Lebih Murah:** Bersepeda dapat menjadi pilihan yang lebih murah dibandingkan dengan menggunakan kendaraan pribadi atau transportasi umum.
- **Kepedulian terhadap Lingkungan:** Bersepeda merupakan pilihan yang ramah lingkungan dan dapat membantu mengurangi polusi udara.

#### Akhir Pekan:

Akhir pekan memiliki jumlah penyewaan kedua tertinggi. Hal ini menunjukkan bahwa banyak orang menggunakan sepeda untuk kegiatan rekreasi dan bersantai di akhir pekan.

#### Hari Libur:

Hari libur memiliki jumlah penyewaan terendah. Hal ini mungkin karena orang-orang memiliki lebih banyak pilihan untuk beraktivitas di hari libur, seperti bepergian atau mengunjungi keluarga.
""", unsafe_allow_html=True)

st.caption('Copyright (c) SerlyADel 2024')
