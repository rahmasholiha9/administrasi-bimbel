import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Sistem Administrasi Bimbel",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS untuk Tampilan Modern & Responsive HP/Laptop
st.markdown("""
    <style>
    /* Styling Latar Belakang & Font Utama */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Banner Premium */
    .header-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.15);
    }
    .header-banner h1 {
        color: white !important;
        margin: 0 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    .header-banner p {
        color: #e0e7ff !important;
        margin: 4px 0 0 0 !important;
        font-size: 0.95rem !important;
    }
    
    /* Styling Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    /* Form & Container styling */
    .stForm {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    /* Tab Navigation Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: pre-wrap;
        border-radius: 8px;
        font-weight: 600;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #eff6ff !important;
        color: #1d4ed8 !important;
    }
    </style>
""", unsafe_allow_html=True)
# Tampilan Header dengan Logo
col_logo, col_text = st.columns([1, 4])

with col_logo:
    # Memanggil file logo yang sudah diunggah di GitHub
    st.image("logo.png", width=120)

with col_text:
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="margin: 0; color: #1e3a8a; font-size: 2rem;">IdeaClass ACADEMY</h1>
            <p style="margin: 0; color: #64748b; font-size: 1rem;">Sistem Administrasi Bimbel • Learn • Grow • Succeed</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
# Initialize Session State
if 'siswa' not in st.session_state:
    st.session_state.siswa = pd.DataFrame(columns=['ID', 'Nama', 'Sekolah', 'OrangTua', 'HP_Ortu', 'Program', 'Status'])
if 'tentor' not in st.session_state:
    st.session_state.tentor = pd.DataFrame(columns=['ID', 'Nama', 'MataPelajaran', 'Tarif_Per_Sesi'])
if 'keuangan' not in st.session_state:
    st.session_state.keuangan = pd.DataFrame(columns=['Tanggal', 'Siswa', 'Jenis', 'Nominal', 'Status'])

# Header Banner
st.markdown("""
    <div class="header-banner">
        <h1>🎓 Sistem Administrasi Bimbel</h1>
        <p>Kelola pendaftaran, data tentor, dan laporan keuangan bimbel dalam satu tempat.</p>
    </div>
""", unsafe_allow_html=True)

# Tab Navigasi Utama
tab_dash, tab_siswa, tab_tentor, tab_keuangan = st.tabs([
    "📊 Dashboard", 
    "👨‍🎓 Data Siswa", 
    "👨‍🏫 Data Tentor", 
    "💳 Keuangan & SPP"
])

# 1. TAB DASHBOARD
with tab_dash:
    col1, col2, col3 = st.columns(3)
    
    total_siswa_aktif = len(st.session_state.siswa[st.session_state.siswa['Status'] == 'Aktif'])
    total_tentor = len(st.session_state.tentor)
    total_pemasukan = st.session_state.keuangan[st.session_state.keuangan['Status'] == 'Lunas']['Nominal'].sum() if not st.session_state.keuangan.empty else 0

    col1.metric("Siswa Aktif", f"{total_siswa_aktif} Orang", "+100% Status Aktif")
    col2.metric("Pengajar / Tentor", f"{total_tentor} Orang", "Tentor Terdaftar")
    col3.metric("Total Cashflow", f"Rp {total_pemasukan:,.0f}", "Pemasukan Terverifikasi")
    
    st.markdown("---")
    st.subheader("📌 Aktivitas Terakhir")
    st.info("Sistem berjalan optimal dan terhubung. Gunakan tab navigasi di atas untuk berpindah menu secara praktis.")

# 2. TAB MANAJEMEN SISWA
with tab_siswa:
    st.subheader("👨‍🎓 Pendaftaran & Kelola Siswa")
    
    with st.expander("➕ Tambah Siswa Baru", expanded=False):
        with st.form("form_siswa_new"):
            c1, c2 = st.columns(2)
            with c1:
                nama = st.text_input("Nama Lengkap Siswa")
                sekolah = st.text_input("Sekolah Asal")
                program = st.selectbox("Program Belajar", ["Reguler", "Privat", "Intensif"])
            with c2:
                ortu = st.text_input("Nama Orang Tua / Wali")
                hp = st.text_input("No. WhatsApp Ortu (Aktif)")
                status = st.selectbox("Status Keanggotaan", ["Aktif", "Non-Aktif", "Alumni"])
            
            submitted = st.form_submit_button("💾 Simpan Data Siswa", use_container_width=True)
            if submitted and nama:
                new_id = f"SIS-{len(st.session_state.siswa) + 1:03d}"
                new_data = pd.DataFrame([[new_id, nama, sekolah, ortu, hp, program, status]], columns=st.session_state.siswa.columns)
                st.session_state.siswa = pd.concat([st.session_state.siswa, new_data], ignore_index=True)
                st.success(f"Siswa **{nama}** ({new_id}) berhasil didaftarkan!")
                st.rerun()

    st.markdown("##### 📋 Daftar Siswa Terdaftar")
    st.dataframe(st.session_state.siswa, use_container_width=True, hide_index=True)

# 3. TAB MANAJEMEN TENTOR
with tab_tentor:
    st.subheader("👨‍🏫 Pendataan Tentor / Pengajar")
    
    with st.expander("➕ Tambah Tentor Baru", expanded=False):
        with st.form("form_tentor_new"):
            c1, c2 = st.columns(2)
            with c1:
                nama_tentor = st.text_input("Nama Lengkap Tentor")
                mapel = st.text_input("Bidang Studi / Mapel")
            with c2:
                tarif = st.number_input("Honor Per Sesi (Rp)", min_value=0, step=10000, value=50000)
            
            sub_tentor = st.form_submit_button("💾 Simpan Data Tentor", use_container_width=True)
            if sub_tentor and nama_tentor:
                t_id = f"TTR-{len(st.session_state.tentor) + 1:03d}"
                new_t = pd.DataFrame([[t_id, nama_tentor, mapel, tarif]], columns=st.session_state.tentor.columns)
                st.session_state.tentor = pd.concat([st.session_state.tentor, new_t], ignore_index=True)
                st.success(f"Tentor **{nama_tentor}** ({t_id}) berhasil ditambahkan!")
                st.rerun()

    st.markdown("##### 📋 Daftar Tentor & Honor")
    st.dataframe(st.session_state.tentor, use_container_width=True, hide_index=True)

# 4. TAB KEUANGAN
with tab_keuangan:
    st.subheader("💳 Pencatatan SPP & Arus Kas")
    
    if not st.session_state.siswa.empty:
        with st.form("form_keuangan_new"):
            c1, c2 = st.columns(2)
            with c1:
                siswa_pilih = st.selectbox("Pilih Siswa", st.session_state.siswa['Nama'].tolist())
                jenis = st.selectbox("Jenis Transaksi", ["SPP Bulanan", "Uang Pendaftaran", "Buku / Modul Belajar"])
            with c2:
                nominal = st.number_input("Nominal Transaksi (Rp)", min_value=0, step=50000, value=150000)
                status_bayar = st.selectbox("Status Pembayaran", ["Lunas", "Belum Lunas"])
            
            sub_bayar = st.form_submit_button("💰 Catat Transaksi Pembayaran", use_container_width=True)
            if sub_bayar:
                tgl = datetime.now().strftime("%Y-%m-%d")
                new_k = pd.DataFrame([[tgl, siswa_pilih, jenis, nominal, status_bayar]], columns=st.session_state.keuangan.columns)
                st.session_state.keuangan = pd.concat([st.session_state.keuangan, new_k], ignore_index=True)
                st.success(f"Transaksi atas nama **{siswa_pilih}** berhasil dicatat!")
                st.rerun()
    else:
        st.warning("⚠️ Tambahkan data siswa terlebih dahulu di tab **Data Siswa** sebelum mencatat pembayaran.")

    st.markdown("##### 📋 Riwayat Arus Kas Pembayaran")
    st.dataframe(st.session_state.keuangan, use_container_width=True, hide_index=True)
