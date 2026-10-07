import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Sistem Administrasi Bimbel", layout="wide")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(worksheet_name):
    return conn.read(worksheet=worksheet_name, ttl="0s")

# Load Data Awal
df_siswa = load_data("Siswa")
df_tentor = load_data("Tentor")
df_keuangan = load_data("Keuangan")

# Menu Navigasi
st.sidebar.title("Bimbel Control Center")
menu = st.sidebar.radio("Navigasi Menu", ["Dashboard", "Manajemen Siswa", "Manajemen Tentor", "Keuangan & SPP"])

# 1. DASHBOARD
if menu == "Dashboard":
    st.title("📊 Dashboard Ringkasan")
    
    col1, col2, col3 = st.columns(3)
    total_siswa = len(df_siswa[df_siswa['Status'] == 'Aktif']) if not df_siswa.empty else 0
    total_tentor = len(df_tentor) if not df_tentor.empty else 0
    
    if not df_keuangan.empty and 'Status' in df_keuangan.columns:
        total_pembayaran = df_keuangan[df_keuangan['Status'] == 'Lunas']['Nominal'].sum()
    else:
        total_pembayaran = 0

    col1.metric("Total Siswa Aktif", total_siswa)
    col2.metric("Total Tentor", total_tentor)
    col3.metric("Total Pemasukan", f"Rp {total_pembayaran:,.0f}")
    
    st.subheader("📌 Aktivitas & Status Sistem")
    st.success("Aplikasi terhubung langsung ke Google Sheets. Data tersimpan permanen!")

# 2. MANAJEMEN SISWA & PENDAFTARAN
elif menu == "Manajemen Siswa":
    st.title("👨‍🎓 Manajemen Siswa & Pendaftaran")
    
    with st.expander("➕ Form Pendaftaran Siswa Baru"):
        with st.form("form_siswa"):
            nama = st.text_input("Nama Lengkap Siswa")
            sekolah = st.text_input("Sekolah Asal")
            ortu = st.text_input("Nama Orang Tua/Wali")
            hp = st.text_input("No. WhatsApp Ortu")
            program = st.selectbox("Program Belajar", ["Reguler", "Privat", "Intensif"])
            status = st.selectbox("Status Siswa", ["Aktif", "Non-Aktif", "Alumni"])
            
            submitted = st.form_submit_button("Simpan Data Siswa")
            if submitted:
                new_id = f"SIS-{len(df_siswa) + 1:03d}"
                new_row = pd.DataFrame([[new_id, nama, sekolah, ortu, hp, program, status]], columns=df_siswa.columns)
                updated_df = pd.concat([df_siswa, new_row], ignore_index=True)
                conn.update(worksheet="Siswa", data=updated_df)
                st.success(f"Siswa {nama} berhasil terdaftar dan tersimpan di Google Sheets!")
                st.rerun()

    st.subheader("📋 Data Siswa Terdaftar")
    st.dataframe(df_siswa, use_container_width=True)

# 3. MANAJEMEN TENTOR
elif menu == "Manajemen Tentor":
    st.title("👨‍🏫 Manajemen Tentor / Guru")
    
    with st.expander("➕ Tambah Data Tentor"):
        with st.form("form_tentor"):
            nama_tentor = st.text_input("Nama Tentor")
            mapel = st.text_input("Bidang Studi / Mapel")
            tarif = st.number_input("Honor Per Sesi (Rp)", min_value=0, step=10000)
            
            sub_tentor = st.form_submit_button("Simpan Data Tentor")
            if sub_tentor:
                t_id = f"TTR-{len(df_tentor) + 1:03d}"
                new_row = pd.DataFrame([[t_id, nama_tentor, mapel, tarif]], columns=df_tentor.columns)
                updated_df = pd.concat([df_tentor, new_row], ignore_index=True)
                conn.update(worksheet="Tentor", data=updated_df)
                st.success(f"Tentor {nama_tentor} berhasil disimpan!")
                st.rerun()

    st.subheader("📋 Daftar Tentor")
    st.dataframe(df_tentor, use_container_width=True)

# 4. KEUANGAN & PEMBAYARAN
elif menu == "Keuangan & SPP":
    st.title("💳 Keuangan & Tagihan SPP")
    
    if not df_siswa.empty:
        with st.form("form_keuangan"):
            siswa_pilih = st.selectbox("Pilih Siswa", df_siswa['Nama'].dropna().tolist())
            jenis = st.selectbox("Jenis Pembayaran", ["SPP Bulanan", "Pendaftaran", "Buku / Modul"])
            nominal = st.number_input("Nominal (Rp)", min_value=0, step=50000)
            status_bayar = st.selectbox("Status", ["Lunas", "Belum Lunas"])
            
            sub_bayar = st.form_submit_button("Catat Transaksi")
            if sub_bayar:
                tgl = datetime.now().strftime("%Y-%m-%d")
                new_row = pd.DataFrame([[tgl, siswa_pilih, jenis, nominal, status_bayar]], columns=df_keuangan.columns)
                updated_df = pd.concat([df_keuangan, new_row], ignore_index=True)
                conn.update(worksheet="Keuangan", data=updated_df)
                st.success("Pembayaran berhasil dicatat ke Google Sheets!")
                st.rerun()
    else:
        st.warning("Belum ada data siswa. Daftarkan siswa terlebih dahulu.")

    st.subheader("📋 Catatan Arus Kas")
    st.dataframe(df_keuangan, use_container_width=True)
