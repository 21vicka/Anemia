import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import datetime
import matplotlib.pyplot as plt

#style 
# Custom CSS for sidebar
def add_sidebar_style():
    st.markdown("""
        <style>
        /* Gaya umum sidebar */
        .css-1d391kg {  
            background-color: #e0f4e8 !important; /* Background hijau muda */
            padding-top: 20px !important;
        }
        /* Tombol sidebar */
        .css-1d391kg .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            font-weight: bold !important;
            padding: 8px 16px !important;
        }
        /* Teks dan judul */
        .css-1d391kg h2, .css-1d391kg p {
            color: #2d6a4f !important;
            font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)


# Fungsi untuk memuat data utama (dataset anemia)
@st.cache_data
def load_data():
    data = pd.read_csv('anemia_set.csv')
    data['Gender'] = data['Gender'].map({1: 'Perempuan', 0: 'Laki-laki'})  # Convert numeric to categorical
    return data

# Fungsi untuk menyimpan riwayat diagnosa ke dalam file CSV
def save_diagnosis(name, gender, hemoglobin, mch, mchc, mcv, result):
    file_path = 'riwayat_diagnosa.csv'
    diagnosis_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.DataFrame([[diagnosis_date, name, gender, hemoglobin, mch, mchc, mcv, result]], 
                        columns=['Tanggal', 'Nama', 'Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV', 'Hasil Diagnosa'])
    try:
        existing_data = pd.read_csv(file_path)
        data = pd.concat([existing_data, data], ignore_index=True)
    except FileNotFoundError:
        pass
    data.to_csv(file_path, index=False)

# Fungsi untuk memuat riwayat diagnosa dari file CSV
def load_diagnosis_history():
    try:
        return pd.read_csv('riwayat_diagnosa.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Tanggal', 'Nama', 'Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV', 'Hasil Diagnosa'])

# Fungsi prediksi anemia
def predict_anemia(model, gender, hemoglobin, mch, mchc, mcv):
    gender = 1 if gender == 'Perempuan' else 0
    data_baru = pd.DataFrame([[gender, hemoglobin, mch, mchc, mcv]], 
                             columns=['Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV'])
    probas = model.predict_proba(data_baru)
    hasil_prediksi = model.predict(data_baru)
    return ("Anemia" if hasil_prediksi[0] == 1 else "Non-Anemia"), probas[0][1]

# Fungsi utama aplikasi
def app():
       # Menambahkan gaya sidebar sebelum komponen lainnya
    add_sidebar_style()


    # Sidebar dengan custom styling
    st.sidebar.header("Ane Minder. ")
    st.title("ANEMINDER")

    # Sidebar untuk navigasi menu
    menu = st.sidebar.selectbox("Pilih Menu", ["Prediksi Anemia", "Riwayat Diagnosa", "Grafik Pemeriksaan"])
    
    # Load dataset
    data = load_data()

    # Split features and labels
    data['Gender'] = data['Gender'].map({'Laki-laki': 0, 'Perempuan': 1})
    X = data[['Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV']]
    y = data['Result']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Create and train Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Menu Prediksi Anemia
    if menu == "Prediksi Anemia":
        st.header("Prediksi Anemia Menggunakan Logistic Regression")
        
        # Akurasi model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        st.write(f'Akurasi model pada data testing: {accuracy * 100:.2f}%')

        # Form input untuk prediksi
        name = st.text_input("Nama Pasien")
        gender_input = st.selectbox("Pilih Gender", options=["Laki-laki", "Perempuan"])
        hemoglobin_input = st.number_input("Berapa Kadar Hemoglobin", min_value=0.0, max_value=20.0, step=0.1)
        mch_input = st.number_input("Berapa Kadar MCH", min_value=0.0, max_value=40.0, step=0.1)
        mchc_input = st.number_input("Berapa Kadar MCHC", min_value=0.0, max_value=40.0, step=0.1)
        mcv_input = st.number_input("Berapa MCV", min_value=0.0, max_value=100.0, step=0.1)

        # Tombol prediksi
        if st.button("Prediksi"):
            if name and hemoglobin_input and mch_input and mchc_input and mcv_input:
                hasil, prob_anemia = predict_anemia(model, gender_input, hemoglobin_input, mch_input, mchc_input, mcv_input)
                st.write(f"Hasil Prediksi: {hasil}")
                st.write(f"Probabilitas Anemia: {prob_anemia:.2f}")
                save_diagnosis(name, gender_input, hemoglobin_input, mch_input, mchc_input, mcv_input, hasil)
                st.success("Data prediksi telah disimpan ke riwayat.")
            else:
                st.warning("Lengkapi semua data untuk prediksi.")

    # Menu Riwayat Diagnosa
    elif menu == "Riwayat Diagnosa":
        st.header("Riwayat Diagnosa")
        history_data = load_diagnosis_history()
        if not history_data.empty:
            st.table(history_data)
        else:
            st.info("Belum ada riwayat diagnosa.")

    # Menu Grafik Pemeriksaan
    elif menu == "Grafik Pemeriksaan":
        st.header("Grafik Pemeriksaan Anemia")
        history_data = load_diagnosis_history()
        if not history_data.empty:
            diagnosis_counts = history_data['Hasil Diagnosa'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 3))
            diagnosis_counts.plot(kind='bar', color=['blue', 'red'], ax=ax)
            ax.set_title("Jumlah Pemeriksaan Berdasarkan Hasil Diagnosa")
            ax.set_xlabel("Hasil Diagnosa")
            ax.set_ylabel("Jumlah")
            st.pyplot(fig)
        else:
            st.info("Belum ada data untuk ditampilkan pada grafik.")

if __name__ == "__main__":
    app()
