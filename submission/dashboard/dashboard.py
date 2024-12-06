import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Menyiapkan DataFrame
def create_byseason_df(df):
    byseason_df = df.groupby(by='season').agg({'cnt': 'sum'}).sort_values(by='cnt')
    return byseason_df

def create_byday_df(df):
    byday_df = df.groupby(by='weekday').agg({'cnt': 'mean'}).sort_values(by='cnt')
    return byday_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by='weathersit').agg({'cnt': 'mean'}).sort_values(by='cnt')
    return byweathersit_df

def create_byuser_df(df):
    byuser_df = df.groupby(by="yr").agg({
    "casual": "sum",
    "registered": "sum",})
    return byuser_df

def create_tren_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    date_group=df.groupby(['year', 'mnth']).agg({'cnt': 'sum'})
    return date_group

main_data = pd.read_csv("main_data.csv")

# Membuat Sidebar
with st.sidebar:
    st.title("Bicycle Rental")
    st.write("Penyewaan Sepeda The Goes")
    # Menambahkan logo perusahaan
    col1, col2, col3 = st.columns([1,5,1])
    with col1:
        st.write(' ')
    with col2:
        st.image("logo_sepeda.png")
    with col3:
        st.write(' ')
    st.write("The Goes adalah perusahaan yang menyediakan layanan penyewaan sepeda. The Goes telah dipercaya oleh banyak pelanggan, baik pengguna terdaftar maupun pengguna biasa.")
    
byseason_df = create_byseason_df(main_data)
byday_df = create_byday_df(main_data)
byweathersit_df = create_byweathersit_df(main_data)
date_group= create_tren_df(main_data)

#Membuat tab
tab1, tab2, tab3= st.tabs(["Penyewaan", "Pengguna","Tren"])

#tab1
with tab1:
    st.header('Bicycle Rental')
    st.subheader('Informasi Terkait Penyewaan Sepeda')
    st.write("Berikut berisi informasi terkait sepeda paling banyak disewa pada tahun 2011 sampai 2012 berdasarkan musim, hari, dan cuaca:")
    
    #Grafik Musim
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.ticklabel_format(style='plain')
    colors_ = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]
    sns.barplot(
        y="cnt", 
        x="season",
        data=byseason_df,
        palette=colors_,
        ax=ax
        )
    ax.set_title("Jumlah Sepeda Sewaan berdasarkan musim", loc="center", fontsize=50)
    ax.set_ylabel("Jumlah sepeda sewaan", fontsize=30)
    ax.set_xlabel("musim", fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.write("""Jumlah total sepeda sewaan pada musim semi (1) sebanyak 471.348, 
             pada musim panas (2) sebanyak 918.589, 
             pada musim gugur (3) sebanyak 1.061.129, 
             pada musim dingin (4) sebanyak 841.613.""")
    st.write(" ")

    #Grafik Hari
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.ticklabel_format(style='plain')
    colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#72BCD4", "#D3D3D3"]
    sns.barplot(
        y="cnt", 
        x="weekday",
        data=byday_df,
        palette=colors_
    )
    ax.set_title("Penyewaan sepeda berdasarkan hari", loc="center", fontsize=50)
    ax.set_ylabel("Rata-rata jumlah penyewaan sepeda", fontsize=30)
    ax.set_xlabel("hari", fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.write("""Rata-rata jumlah penyewaan sepeda pada hari Minggu (0) sebanyak 4.228,8, 
             pada hari Senin (1) sebanyak 4.338,12, 
             pada hari Selasa (2) sebanyak 4.510,66, 
             pada hari Rabu (3) sebanyak 4.548,54,
             pada hari Kamis (4) sebanyak 4.667,25,
             pada hari Jumat (5) sebanyak 4.690,28,
             pada hari Sabtu (6) sebanyak 4.550,54.""")
    st.write(" ")

    # Grafik Cuaca
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.ticklabel_format(style='plain')
    colors_ = ["#72BCD4","#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="cnt", 
        x="weathersit",
        data=byweathersit_df,
        palette=colors_
    )
    ax.set_title("Penyewaan sepeda berdasarkan cuaca", loc="center", fontsize=50)
    ax.set_ylabel("Rata-rata jumlah penyewaan sepeda", fontsize=30)
    ax.set_xlabel("Cuaca", fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.write("""Rata-rata jumlah penyewaan sepeda saat cuaca cerah (1) sebanyak 4.876,78, 
             saat cuaca kabut (2) sebanyak 4.035,86, 
             saat cuaca salju ringan (3) sebanyak 4.510,66, 
             saat cuaca hujan lebat (4) sebanyak 0.
             """)
    st.write(" ")

#tab 2
with tab2:
    st.header('Bicycle Rental')
    st.subheader('Informasi Terkait Perbandingan Pengguna')
    st.write("Berikut berisi informasi terkait perbandingan antara pengguna terdaftar dan pengguna biasa pada tahun 2011 dan 2012")
    # Membuat kolom
    col1, col2= st.columns(2)
    with col1:
        # Membuat pie chart 2011
        fig, ax = plt.subplots(figsize=(5, 5))
        Total2011=(247252,995851)
        colors = ('#8B4513', '#93C572')
        plt.pie(
            x=Total2011,
            labels=["Casual","Registered"],
            autopct='%1.1f%%',
            colors=colors,
            textprops={'fontsize': 20}
        )
        ax.set_title('Tahun 2011', fontsize=20)
        st.pyplot(fig)
    
    with col2:
        # Membuat pie chart 2012
        fig, ax = plt.subplots(figsize=(5, 5))
        Total2012=(372765,1676811)
        colors = ('#8B4513', '#93C572')
        plt.pie(
            x=Total2012,
            labels=["Casual","Registered"],
            autopct='%1.1f%%',
            colors=colors,
            textprops={'fontsize': 20}
        )
        ax.set_title('Tahun 2012', fontsize=20)
        st.pyplot(fig)
    st.write(
            """Terlihat pada pie chart sebelah kiri bahwa persentase jumlah pengguna terdaftar pada tahun 2011 adalah 80,1%, 
            sedangkan persentase jumlah pengguna biasa pada tahun 2011 adalah 19,9%. 
            Terlihat pada pie chart sebelah kanan bahwa persentase jumlah pengguna terdaftar pada tahun 2012 adalah 81,8%, 
            sedangkan persentase jumlah pengguna biasa pada tahun 2012 adalah 18,2%. 
            Berdasarkan kedua pie chart di atas, diketahui bahwa jumlah sepeda yang disewa oleh pengguna terdaftar lebih banyak daripada pengguna biasa untuk tahun 2011 dan 2012.
            """)

# tab 3
with tab3:
    st.header('Bicycle Rental')
    st.subheader('Tren Penyewaan Sepeda')
    st.write("Berikut berisi informasi terkait tren penyewaan sepeda tahun 2011 dan 2012")
    # Membuat grafik tren penyewaan sepeda 2011 dan 2012
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.lineplot(data=date_group, x='mnth', y="cnt", hue='year', palette="dark")
    ax.set_title("Tren Penyewaan Sepeda Tahun 2011 dan 2012", loc="center", fontsize=50)
    ax.set_ylabel("Jumlah Sepeda yang Disewa", fontsize=20)
    ax.set_xlabel("bulan", fontsize=20)
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    plt.legend(fontsize=30)
    st.pyplot(fig)

    st.write("Jika ingin menampilkan lebih banyak data, silahkan klik di bawah ini")
    agree = st.checkbox('Tampilkan Data')
    if agree:
        st.write(date_group)