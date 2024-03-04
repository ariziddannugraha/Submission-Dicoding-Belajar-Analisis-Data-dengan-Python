import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
import streamlit.components.v1 as components

df = pd.read_csv("main_data.csv")

# Filter data
min_date = pd.to_datetime(df['dteday']).dt.date.min()
max_date = pd.to_datetime(df['dteday']).dt.date.max()

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df



######################################   

with st.sidebar:
    st.text('Choose Wisely')
    st.image('https://media.giphy.com/media/3o7abqxwe7kj2DRcqY/giphy.gif?cid=790b7611poi5jqsgvkzpbww25ave8vb43hlevrv2j3kqk0xj&ep=v1_gifs_search&rid=giphy.gif&ct=g')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

    tahun = st.selectbox(
        label="Filter tahun*",
        options=(2011, 2012, "2011-2012")
    )

    st.caption("*hanya untuk pertanyaan 1")

    on = st.toggle("Tampilkan dataset")

    st.caption("Ari Ziddan Nugraha")


main_df = df[(df['dteday'] >= str(start_date)) & 
                (df['dteday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)

# Membuat judul
st.header('Bike Sharing Rental')

###############################

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total User', value= daily_rent_total)

################################
fig = plt.figure()

daily_rent_casual = daily_casual_rent_df['casual'].sum()
daily_rent_registered = daily_registered_rent_df['registered'].sum()
daily_rent_total = daily_rent_df['cnt'].sum()

user = [daily_rent_casual, daily_rent_registered]
label = ("casual", "registered")
plt.pie(
    x=user,
    labels=label,
    wedgeprops = {'width': 0.4},
    autopct='%1.1f%%'
)
# plt.set_title('Daily Bike Rentals')
st.pyplot(fig)
st.write("{} Total User".format(daily_rent_total))

if on:
    st.subheader('Dataset review')
    main_df

################################

st.subheader('Pertanyaan 1')

st.write("Pada saat musim apa bike riding mendapatkan order terbanyak dalam satu tahun?")
# Pivot table berdasarkan musim dan tahun
#jika pertahun
if isinstance(tahun, (int)):
    dfyr = df[df['yr'] == tahun]
    by_season = dfyr.pivot_table(index='yr', columns='season', values='cnt', aggfunc='sum')
#jika dua tahun
else:
    by_season = df.pivot_table(index='yr', columns='season', values='cnt', aggfunc='sum')

ax = by_season.plot(kind="bar", figsize=(10,5))
ax.set_xlabel('Tahun')
ax.set_ylabel('Count')
st.pyplot(plt.gcf())

with st.expander("**Kesimpulan pertanyaan 1**"):
    st.write("""
    Dilihat dari data dan juga visualisasinya, musim panas merupakan musim favorit bagi para penyewa sepeda,
    disusul musim semi, musim gugur, dan diurutan terakhir musim dingin. Musim panas menjadi musim favorit karena musim tersebut merupakan
    waktu libur bagi para pelajar, sehingga bermain sepeda dan mobilisasi menggunakan sepeda bisa menjadi alternatif untuk berpergian.

    """
    )


################################

st.subheader('Pertanyaan 2')

st.write("Apakah cuaca mempengaruhi order terhadap bike sharing?")
by_weather = main_df.pivot_table(index='yr', columns='weathersit', values='cnt', aggfunc='sum')
ax = by_weather.plot(kind="bar", figsize=(10,5))
ax.set_xlabel("Tahun")
ax.set_ylabel("Count")
st.pyplot(plt.gcf())

with st.expander("**Kesimpulan pertanyaan 2**"):
    st.write("""
    Visualisasi yang sudah dibuat menjelaskan bahwa cuaca sangat mempengaruhi penentuan penyewaan sepeda. Cuaca cerah merupakan cuaca
    dengan penyewa terbanyak baik pada tahun 2011 maupun 2012. Diikuti dengan cuaca berkabut, dan salju ringan. Penyewaan berdasarkan
    cuaca memiliki kesamaan pola atau trean antara dua tahun tersebut. Sebagai tambahan, pada cuaca hujan lebat tidak memiliki penyewa
    sama sekali, karena cuaca ekstrem tersebut tidak memungkinkan untuk orang bersepeda.
    """
    )