import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistem Administrasi Bimbel", layout="wide")

# Database sementara menggunakan session state
if 'siswa' not in st.session_state:
    st.session_state.siswa = pd.DataFrame(columns=['ID', 'Nama', 'Sekolah', 'OrangTua', 'HP_Ortu', 'Program', 'Status'])
if 'tentor' not in st.session_state:
    st.session_state.tentor = pd.DataFrame(columns=['ID', 'Nama', 'MataPelajaran', 'Tarif_Per_Sesi'])
if 'keuangan' not in st.session_state:
    st.session_state.keuangan = pd.DataFrame(columns=['Tanggal', 'Siswa', 'Jenis', 'Nominal', 'Status'])

# Menu Navigasi
st.sidebar.title("Bimbel Control Center")
menu = st.sidebar.radio("Navigasi Menu", ["Dashboard", "Manajemen Siswa", "Manajemen Tentor", "Keuangan & SPP"])

# 1. DASHBOARD
if menu == "Dashboard":
    st.title("📊 Dashboard Ringkasan")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Siswa Aktif", len(st.session_state.siswa[st.session_state.siswa['Status'] == 'Aktif']))
    col2.metric("Total Tentor", len(st.session_state.tentor))
    
    total_pembayaran = st.session_state.keuangan[st.session_state.keuangan['Status'] == 'Lunas']['Nominal'].sum() if not st.session_state.keuangan.empty else 0
    col3.metric("Total Pemasukan", f"Rp {total_pembayaran:,.0f}")
    
    st.subheader("📌 Aktivitas & Status Sistem")
    st.success("Aplikasi Administrasi Bimbel Berhasil Berjalan!")

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
                new_id = f"SIS-{len(st.session_state.siswa) + 1:03d}"
                new_data = pd.DataFrame([[new_id, nama, sekolah, ortu, hp, program, status]], columns=st.session_state.siswa.columns)
                st.session_state.siswa = pd.concat([st.session_state.siswa, new_data], ignore_index=True)
                st.success(f"Siswa {nama} berhasil didaftarkan!")
                st.rerun()

    st.subheader("📋 Data Siswa Terdaftar")
    st.dataframe(st.session_state.siswa, use_container_width=True)

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
                t_id = f"TTR-{len(st.session_state.tentor) + 1:03d}"
                new_t = pd.DataFrame([[t_id, nama_tentor, mapel, tarif]], columns=st.session_state.tentor.columns)
                st.session_state.tentor = pd.concat([st.session_state.tentor, new_t], ignore_index=True)
                st.success(f"Tentor {nama_tentor} berhasil ditambahkan!")
                st.rerun()

    st.subheader("📋 Daftar Tentor")
    st.dataframe(st.session_state.tentor, use_container_width=True)

# 4. KEUANGAN & PEMBAYARAN
elif menu == "Keuangan & SPP":
    st.title("💳 Keuangan & Tagihan SPP")
    
    if not st.session_state.siswa.empty:
        with st.form("form_keuangan"):
            siswa_pilih = st.selectbox("Pilih Siswa", st.session_state.siswa['Nama'].tolist())
            jenis = st.selectbox("Jenis Pembayaran", ["SPP Bulanan", "Pendaftaran", "Buku / Modul"])
            nominal = st.number_input("Nominal (Rp)", min_value=0, step=50000)
            status_bayar = st.selectbox("Status", ["Lunas", "Belum Lunas"])
            
            sub_bayar = st.form_submit_button("Catat Transaksi")
            if sub_bayar:
                tgl = datetime.now().strftime("%Y-%m-%d")
                new_k = pd.DataFrame([[tgl, siswa_pilih, jenis, nominal, status_bayar]], columns=st.session_state.keuangan.columns)
                st.session_state.keuangan = pd.concat([st.session_state.keuangan, new_k], ignore_index=True)
                st.success("Pembayaran berhasil dicatat!")
                st.rerun()
    else:
        st.warning("Silakan isi data siswa terlebih dahulu pada menu 'Manajemen Siswa'.")

    st.subheader("📋 Catatan Arus Kas")
    st.dataframe(st.session_state.keuangan, use_container_width=True)
