#libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)


#ambil data 
@st.cache_data
def load_day():
    day = pd.read_csv("day.csv")
    day["dteday"] = pd.to_datetime(day["dteday"])
    day = day.sort_values("dteday")
    return day

@st.cache_data
def load_hour():
    hour = pd.read_csv("hour.csv")
    hour["dteday"] = pd.to_datetime(hour["dteday"])
    return hour

day = load_day()
hour = load_hour()

#sidebar 
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Kelompok",
         "Overview",
         "P1: Distribusi cnt per jam",
         "P2: Tren 3 bulanan",
         "P3: Rata‑rata per minggu",
         "P4: Sebaran per musim",
         "P5: Korelasi suhu–cnt",
         "P6: Distribusi suhu",
         "Perbandingan Antar Data",
         "Saran dari Hasil Analisis"],
        icons=["house","people","graph-up","calendar3","cloud-sun","thermometer-half","fuel-pump","thermometer-half","graph-up-arrow","lightbulb"],
        default_index=0
    )


#Identitas kelompok kami
if selected == "Kelompok":
    st.title("UAS Analisis Data Bike Sharing Dataset")

    st.subheader("Identitas Kelompok")
    st.markdown("""
    - Kelas : IF-2  
    - Anggota:  
        - 10124056 – Moch. Albany Alfachrezi Syechan            (membuat streamlit,membuat analisis pertanyaan 3 dan 4 di file pra uts dan uas)  
        - 10124044 – Ichza Mutawalli Razzaq                     (membuat hasil analisis dari perbandingan data,dan pertanyaan 2 di file uas dan pra uts)  
        - 10124080 – Advent G. Sihombing                        (membuat hasil analisis dari pertanyaan 2 dan ringkasan data "overview" di file pra uts dan uas)
        - 10124079 – Andi Muhamad Hakim R.M                     (membuat hasil analisi dari pertanyaan 1 dan saran dari hasil analisis di file pra uts dan uas)
        - 10124059 – Yusya Raditya(membuat                      (membuat hasil analisis dari pertanyaan 5 dan 6 di file pra uts dan uas)  
        - 10124473 – Bayu Ilham Samudra                         (-)
        """)

#halaman overview
elif selected == "Overview":
    st.title("Proyek Analisis Data: Bike Sharing Dataset")
    st.subheader("Pertanyaan")
    st.markdown("""
    1. Distribusi jumlah penyewa (`cnt`) setiap **jam** (hour.csv).
    2. Tren jumlah penyewa per **3 bulan** tahun 2011–2012 (day.csv).
    3. Rata‑rata jumlah penyewa per **hari dalam seminggu** (day.csv).
    4. Perbedaan sebaran jumlah penyewa (`cnt`) berdasarkan **musim** (day.csv).
    5. Hubungan **suhu (`temp`)** dengan jumlah penyewa (`cnt`) (day.csv).
    6. Distribusi **suhu (`temp`)** sepanjang pengamatan (day.csv).
    """)
    st.subheader("Ringkasan Data")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dataset `day.csv`")
        st.write(day.head())
        st.write(day.describe(include="all"))
    with col2:
        st.write("Dataset `hour.csv`")
        st.write(hour.head())
        st.write(hour.describe(include="all"))



#Distribusi cnt per jam
elif selected == "P1: Distribusi cnt per jam":
    st.title("P1 – Distribusi Jumlah Penyewa per Jam (hour.csv)")


    fig, ax = plt.subplots(figsize=(8,4))
    ax.hist(hour["cnt"], bins=40, color="steelblue", edgecolor="black", alpha=0.8)
    ax.set_xlabel("Jumlah penyewa per jam (cnt)")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Histogram jumlah penyewa per jam")
    st.pyplot(fig)

    st.markdown("Beberapa statistik deskriptif untuk `cnt` per jam:")
    st.write(hour["cnt"].describe())
    
    st.markdown("""
    Hasil Analisis: distribusi `cnt` per jam cenderung miring ke kanan (right‑skewed) 
    banyak jam dengan penyewaan rendah,sedikit jam dengan penyewaan tinggi.
    """)



#Tren jumlah penyewa per 3 bulan
elif selected == "P2: Tren 3 bulanan":
    st.title("P2 – Tren Jumlah Penyewa per 3 Bulan (2011–2012)")

    st.markdown("""
    agregasi 3 bulanan.
    """)

    #data day 3 bulanan yaitu 1: Jan–Mar, 2: Apr–Jun, 3: Jul–Sep, 4: Okt–Des
    day_q = day.copy()
    day_q["quarter3"] = ((day_q["mnth"] - 1) // 3) + 1
    agg_q = (
        day_q
        .groupby(["yr", "quarter3"], as_index=False)["cnt"]
        .mean()
        .sort_values(["yr", "quarter3"])
    )

    st.dataframe(agg_q)

    fig, ax = plt.subplots(figsize=(8,4))
    for year, dsub in agg_q.groupby("yr"):
        label = f"Tahun {2011 + year}"
        ax.plot(dsub["quarter3"], dsub["cnt"], marker="o", label=label)
    ax.set_xticks([1,2,3,4])
    ax.set_xticklabels(["Q1 (Jan–Mar)","Q2 (Apr–Jun)","Q3 (Jul–Sep)","Q4 (Okt–Des)"])
    ax.set_xlabel("Kuartal (3 bulanan)")
    ax.set_ylabel("Rata‑rata cnt per hari")
    ax.set_title("Tren jumlah penyewa per 3 bulan (2011–2012)")
    ax.grid(alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    st.markdown("""
   Hasil Analisis:
    - Tren meningkat dari awal tahun menuju pertengahan tahun.
    - Puncak sekitar musim panas/gugur,lalu turun lagi di akhir tahun.
    """)


#Rata rata jumlah penyewa per minggu
elif selected == "P3: Rata‑rata per minggu":
    st.title("P3 – Rata‑rata Jumlah Penyewa per Hari dalam Seminggu")


    weekday_map = {
        0: "Minggu",
        1: "Senin",
        2: "Selasa",
        3: "Rabu",
        4: "Kamis",
        5: "Jumat",
        6: "Sabtu",
    }

    avg_weekday = (
        day
        .groupby("weekday", as_index=False)["cnt"]
        .mean()
        .sort_values("weekday")
    )
    avg_weekday["weekday_name"] = avg_weekday["weekday"].map(weekday_map)

    st.dataframe(avg_weekday[["weekday","weekday_name","cnt"]])

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(avg_weekday["weekday_name"], avg_weekday["cnt"], color="skyblue", edgecolor="black")
    ax.set_xlabel("Hari dalam seminggu")
    ax.set_ylabel("Rata‑rata cnt per hari")
    ax.set_title("Rata‑rata penyewa per weekday")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

    st.markdown("""
    Hasil Analisis:
    - Hari kerja (Senin–Jumat) cenderung memiliki jumlah penyewa lebih tinggi.
    - Puncak biasanya Kamis/Jumat,akhir pekan sedikit menurun.
    """)


#Sebaran cnt berdasarkan musim
elif selected == "P4: Sebaran per musim":
    st.title("P4 – Sebaran Jumlah Penyewa Berdasarkan Musim (day.csv)")


    season_map = {
        1: "Musim Dingin",
        2: "Musim Semi",
        3: "Musim Panas",
        4: "Musim Gugur",
    }

    data_box = [day[day["season"] == s]["cnt"] for s in [1,2,3,4]]
    labels = [season_map[s] for s in [1,2,3,4]]

    fig, ax = plt.subplots(figsize=(8,5))
    ax.boxplot(data_box, labels=labels)
    ax.set_ylabel("Jumlah penyewa per hari (cnt)")
    ax.set_title("Sebaran jumlah penyewa per musim")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

    st.markdown("""
    Hasil Analisis:
    - Musim dingin: median terendah, permintaan rendah dan konsisten.
    - Musim semi: median menengah,variasi lebih tinggi.
    - Musim panas: median tinggi,banyak outlier atas.
    - Musim gugur: median tertinggi dan cukup konsisten.
    """)


#Hubungan suhu temp dengan cnt
elif selected == "P5: Korelasi suhu–cnt":
    st.title("P5 – Apakah Suhu temp Berhubungan dengan Jumlah Penyewa (cnt)?")


    corr = day["temp"].corr(day["cnt"])
    st.write(f"Koefisien korelasi Pearson antara `temp` dan `cnt` = **{corr:.3f}**")

    fig, ax = plt.subplots(figsize=(8,5))
    ax.scatter(day["temp"], day["cnt"], alpha=0.4, s=20, color="tomato", edgecolors="k", linewidths=0.2)
    ax.set_xlabel("Suhu ternormalisasi (temp)")
    ax.set_ylabel("Jumlah penyewa per hari (cnt)")
    ax.set_title("Scatter plot suhu vs jumlah penyewa")
    ax.grid(alpha=0.3)
    st.pyplot(fig)

    st.markdown("""
    Hasil Analisis:
    - Ada hubungan positif cukup kuat: semakin hangat sampai titik tertentu sehingga penyewaan meningkat.
    - Pada suhu sangat tinggi,kenaikan mulai melandai.
    """)


#Distribusi suhu temp
elif selected == "P6: Distribusi suhu":
    st.title("P6 – Distribusi Suhu (temp) Sepanjang Pengamatan")


    fig, ax = plt.subplots(figsize=(8,4))
    ax.hist(day["temp"], bins=30, color="seagreen", edgecolor="black", alpha=0.8)
    ax.set_xlabel("Suhu ternormalisasi (temp)")
    ax.set_ylabel("Frekuensi hari")
    ax.set_title("Histogram suhu (temp) – day.csv")
    ax.grid(axis="y", alpha=0.3)
    st.pyplot(fig)

    st.write("Statistik deskriptif `temp` (day.csv):")
    st.write(day["temp"].describe())

    st.markdown("""
   Hasil Analisis:
    - Rentang `temp` sekitar 0.06 – 0.86, mayoritas di kisaran menengah 0.3–0.7.
    - Rentang ini kira‑kira ekuivalen 12–28°C sehingga nyaman untuk bersepeda).
    - Hampir tidak ada nilai ekstrem mendekati 0 atau 1 (suhu sangat dingin/panas).
    """)

#Perbandigan Antar Data
elif selected == "Perbandingan Antar Data":

    tab1, tab2, tab3 = st.tabs(["Heatmap Korelasi", "Regresi Multivariabel", "Clustering Jam"])

    #Heatmap korelasi
    with tab1:
        st.subheader("Heatmap Korelasi Variabel(day.csv)")
        num_cols = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
        corr_matrix = day[num_cols].corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, ax=ax)
        st.pyplot(fig)

        st.markdown("""
        **Hasil Analisis:**  
        - `temp` dan `atemp` sangat berkorelasi(multikolinearitas tinggi).  
        - `cnt` berkorelasi kuat dengan `temp` dan `registered`.  
        - `hum` cenderung berkorelasi negatif kecil terhadap `cnt`.
        """)

    #Regresi multivariabel
    with tab2:
        st.subheader("Regresi Linear: cnt ~ temp + workingday + season")

        X = day[["temp", "workingday", "season"]]
        y = day["cnt"]
        model = LinearRegression()
        model.fit(X, y)
        r2 = model.score(X, y)

        coef_df = pd.DataFrame({
            "Variabel": ["Intercept"] + list(X.columns),
            "Koefisien": [model.intercept_] + list(model.coef_)
        })
        st.write("Koefisien model:")
        st.dataframe(coef_df)

        st.metric("R² Model Multivariabel", f"{r2:.3f}")

        st.markdown("""
        **Hasil Analisis:**  
        - Koefisien `temp` positif,setiap kenaikan unit `temp` akan menaikkan `cnt` rata-rata sesuai koefisien.  
        - `workingday` dan `season` memberi efek tambahan sesuai konteks hari kerja dan musim.
        """)

    #Clustering jam
    with tab3:
        st.subheader("K-Means Clustering: Segmentasi Jam Penyewaan(hour.csv)")

        features = ["temp", "hum", "cnt"]
        data_clust = hour[features].copy()

        scaler = StandardScaler()
        scaled = scaler.fit_transform(data_clust)

        kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
        data_clust["cluster"] = kmeans.fit_predict(scaled)

        fig = px.scatter_3d(
            data_clust,
            x="temp", y="hum", z="cnt",
            color="cluster",
            title="Cluster jam berdasarkan temp, hum, cnt",
            opacity=0.7
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("Rata-rata tiap cluster:")
        st.dataframe(
            data_clust.groupby("cluster")["cnt"].agg(["mean", "count"]).round(0)
        )

        st.markdown("""
        **Hasil Analisis jika dianalogikan sebagai contoh:**  
        - Cluster 0: jam sibuk dengan `cnt` tinggi, suhu nyaman.  
        - Cluster 1: jam sepi dengan `cnt` rendah (malam atau cuaca buruk).  
        - Cluster 2: jam menengah (rekreasi/akhir pekan).
        """)
#saran
elif selected == "Saran dari Hasil Analisis":
    st.title("Saran")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - Ketika jam sibuk lebih baik tambah unit,dan ketika hujan berikan diskon karena di saat kondisi itu akan sepi  
        - Musim panas dan gugur kita bisa memperluas unit ke area pusat kota dan tambahkan unit karena di saat itu banyak hari libur.  
        - Musim dingin diakibatkan akan menurunkan suhu maka gunakan untuk perawatan unit karena dikhawatirkan sepi di saat kondisi itu.
        """)











