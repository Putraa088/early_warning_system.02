import streamlit as st

def show_panduan_page():
    """Display the manual book/guide page"""
    
    st.markdown("""
    <style>
    .manual-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .toc-container {
        background: rgba(255,255,255,0.05);
        padding: 25px;
        border-radius: 10px;
        margin: 25px 0;
        border-left: 4px solid #00a8ff;
    }
    .section-card {
        background: rgba(255,255,255,0.02);
        padding: 25px;
        border-radius: 10px;
        margin: 25px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .section-title {
        color: #00a8ff;
        border-bottom: 2px solid #00a8ff;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .step-box {
        background: rgba(0,168,255,0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #00a8ff;
    }
    .warning-box {
        background: rgba(255,193,7,0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #ffc107;
    }
    .info-box {
        background: rgba(40,167,69,0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #28a745;
    }
    .contact-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 25px;
        border-radius: 10px;
        margin: 30px 0;
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="manual-header">
        <h1 style="margin:0; color:white; font-size:2.5rem;"> PANDUAN PENGGUNAAN SISTEM</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:1.2rem;">
            Manual Book Lengkap untuk Early Warning System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ **Panduan ini menjelaskan cara menggunakan semua fitur di website Early Warning System.**")
    
    # Table of Contents
    with st.expander(" **DAFTAR ISI**", expanded=True):
        st.markdown("""
        ### **Navigasi Cepat:**
        1. [Halaman Utama (Home)](#halaman-utama-home)
        2. [Halaman Lapor Banjir](#halaman-lapor-banjir)
        3. [Halaman Catatan Laporan](#halaman-catatan-laporan)
        4. [Halaman Prediksi Real-time](#halaman-prediksi-real-time)
        5. [Halaman Simulasi Banjir](#halaman-simulasi-banjir)
        6. [Panduan Umum](#panduan-umum)
        7. [Dukungan Teknis](#dukungan-teknis)
        """)
    
    st.markdown("---")
    
    # ==================== 1. HALAMAN UTAMA ====================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="halaman-utama-home"> 1. HALAMAN UTAMA (HOME)</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Deskripsi**
    Halaman utama memberikan gambaran umum tentang sistem peringatan dini banjir. 
    Ini adalah titik masuk pertama untuk pengguna baru.
    """)
    
    st.markdown("""
    ### **Cara Menggunakan**
    1. **Baca informasi pengantar** di bagian atas halaman untuk memahami tujuan sistem
    2. **Baca bagian "Tentang Sistem"** untuk mengetahui fungsi utama website
    3. **Baca bagian "Manfaat Sistem"** untuk memahami nilai yang diberikan
    4. **Gunakan sidebar navigasi** di sebelah kiri untuk berpindah ke halaman lain
    """)
    
    st.markdown("""
    ### **Elemen Utama**
    - **Judul Sistem:** "SISTEM PERINGATAN DINI BANJIR"
    - **Deskripsi Singkat:** Penjelasan tentang platform monitoring dan prediksi banjir
    - **Sidebar Navigasi:** Menu untuk berpindah antar halaman
    - **Informasi Kontak:** Alamat, email, dan telepon untuk menghubungi tim
    """)
    
    st.markdown("""
    ### **Navigasi dari Halaman Ini**
    - Klik **"Lapor Banjir"** untuk melaporkan kejadian banjir
    - Klik **"Catatan Laporan"** untuk melihat laporan yang sudah masuk
    - Klik **"Prediksi Real-time"** untuk melihat kondisi terkini
    - Klik **"Simulasi Banjir"** untuk melakukan prediksi manual
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 2. HALAMAN LAPOR BANJIR ====================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="halaman-lapor-banjir"> 2. HALAMAN LAPOR BANJIR</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Deskripsi**
    Halaman untuk melaporkan kejadian banjir di lokasi tertentu. 
    Data yang dilaporkan akan digunakan untuk analisis dan pemantauan.
    """)
    
    st.markdown("""
    ### **Cara Menggunakan**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="step-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **1. Isi Alamat Lengkap**
        - Masukkan alamat kejadian banjir dengan detail
        - Contoh: "Jl. Merdeka No. 12, RT 05/RW 02, Kelurahan Sukamaju"
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="step-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **2. Pilih Tinggi Banjir**
        Pilih salah satu dari empat kategori:
        - Setinggi mata kaki
        - Setinggi betis
        - Setinggi lutut
        - Lebih dari lutut
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="step-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **3. Isi Data Pelapor**
        - **Nama Lengkap:** Masukkan nama Anda
        - **Nomor Telepon:** Masukkan nomor yang bisa dihubungi (opsional)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="step-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **4. Unggah Foto**
        - Klik tombol "Pilih file"
        - Pilih foto kondisi banjir dari perangkat Anda
        - Format: JPG, JPEG, PNG
        - **WAJIB** mengunggah foto
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    #### **5. Kirim Laporan**
    - Klik tombol "Kirim Laporan"
    - Tunggu konfirmasi keberhasilan
    - Jika ada error, perbaiki data yang diminta
    """)
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    ### **Validasi Form**
    - Alamat harus diisi
    - Tinggi banjir harus dipilih (bukan "Pilih tinggi banjir")
    - Nama pelapor harus diisi
    - Foto harus diunggah
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Setelah Mengirim**
    - Sistem akan menampilkan pesan sukses atau error
    - Laporan akan tersimpan di database
    - Data dapat dilihat di halaman "Catatan Laporan"
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 3. HALAMAN CATATAN LAPORAN ====================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="halaman-catatan-laporan"> 3. HALAMAN CATATAN LAPORAN</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Deskripsi**
    Halaman untuk melihat dan menganalisis laporan banjir yang telah dikirimkan oleh masyarakat.
    """)
    
    st.markdown("""
    ### **Struktur Halaman**
    Halaman ini memiliki dua sub-halaman:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **A. Menu Utama Catatan Laporan**
        - **Tombol "Lihat Laporan Harian"** → menuju ke laporan hari ini
        - **Tombol "Lihat Rekapan Bulanan"** → menuju ke statistik bulanan
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        #### **B. Navigasi Antar Sub-halaman**
        - **Kembali ke Menu:** Tombol "Kembali" di pojok kiri atas
        - **Pilih Tab:** Untuk halaman bulanan ada tab pilihan
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    #### **B.1 Laporan Harian**
    1. **Lihat daftar laporan** yang tercatat hari ini
    2. **Setiap laporan menampilkan:**
       - Nomor urut
       - Alamat kejadian
       - Waktu pelaporan (format HH:MM)
       - Tinggi banjir
       - Nama pelapor
    
    3. **Lihat Foto (jika ada):**
       - Klik tombol "Lihat" di kolom foto
       - Foto akan muncul dalam panel expandable
    
    4. **Analisis Statistik:**
       - Scroll ke bawah untuk melihat analisis harian
       - Lihat jumlah total laporan
       - Lihat jumlah lokasi berbeda
       - Lihat jumlah pelapor berbeda
    """)
    
    st.markdown("""
    #### **B.2 Rekapan Bulanan**
    1. **Pilih Tab:**
       - Tab "Laporan Bulan Ini" → daftar laporan bulan berjalan
       - Tab "Statistik 1 Tahun" → grafik dan analisis 12 bulan
    
    2. **Untuk Tab "Laporan Bulan Ini":**
       - Lihat statistik bulanan di bagian atas
       - Scroll melalui daftar laporan
       - Format tanggal: "Hari, DD/MM/YYYY"
    
    3. **Untuk Tab "Statistik 1 Tahun":**
       - Lihat grafik batang distribusi laporan
       - Analisis tren peningkatan/penurunan
       - Download data CSV untuk analisis lebih lanjut
       - Identifikasi bulan dengan laporan tertinggi
    """)
    
    st.markdown("""
    ### **Fitur Khusus**
    - **Highlight laporan hari ini** dengan badge waktu
    - **Filter otomatis** berdasarkan tanggal
    - **Visualisasi data** untuk analisis cepat
    - **Export data** dalam format CSV
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 4. HALAMAN PREDIKSI REAL-TIME ====================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="halaman-prediksi-real-time"> 4. HALAMAN PREDIKSI REAL-TIME</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Deskripsi**
    Halaman untuk memantau kondisi dan prediksi banjir berdasarkan data real-time dari BBWS Bengawan Solo.
    """)
    
    st.markdown("""
    ### **Cara Menggunakan**
    1. **Lihat Status Keseluruhan:**
       - Perhatikan banner warna di bagian atas:
         - **Hijau (RENDAH)** → kondisi aman
         - **Kuning (MENENGAH)** → waspada
         - **Merah (TINGGI)** → kondisi kritis
    """)
    
    st.markdown("""
    2. **Pantau Data Real-time:**
       - **Tinggi Air Terkini:** Level air dalam meter di atas permukaan laut
       - **Curah Hujan:** Volume hujan per jam dalam mm
       - **Update Terakhir:** Waktu pembaruan data terakhir
    """)
    
    st.markdown("""
    3. **Analisis per Lokasi:**
       Sistem menampilkan 3 lokasi pemantauan:
       1. Ngadipiro (S. keduang)
       2. Wonogiri Dam (Spillway)
       3. Colo Weir (S. bengawan solo)
       
       Untuk setiap lokasi, lihat:
       - Tinggi air dan statusnya
       - Progress bar prediksi AI (Neural Network)
       - Progress bar analisis statistik (Distribusi Gumbel)
    """)
    
    st.markdown("""
    4. **Detail Prediksi (Opsional):**
       - Klik panah "Detail Prediksi" untuk informasi lebih dalam
       - Lihat risk level numerik
       - Baca analisis dari masing-masing metode
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### **🟢 RENDAH**
        Risk level: 0.0-0.5
        Status: Kondisi normal
        """)
    
    with col2:
        st.markdown("""
        ### **🟡 MENENGAH**
        Risk level: 0.5-0.8
        Status: Perlu pemantauan
        """)
    
    with col3:
        st.markdown("""
        ### **🔴 TINGGI**
        Risk level: 0.8-1.0
        Status: Potensi banjir tinggi
        """)
    
    st.markdown("""
    ### **Sumber Data**
    - Data berasal dari BBWS Bengawan Solo
    - Update dilakukan secara berkala
    - Prediksi menggunakan dua metode: AI dan statistik
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 5. HALAMAN SIMULASI BANJIR ====================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="halaman-simulasi-banjir"> 5. HALAMAN SIMULASI BANJIR</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Deskripsi**
    Halaman kalkulator interaktif untuk memprediksi risiko banjir berdasarkan parameter cuaca yang dimasukkan manual.
    """)
    
    st.markdown("""
    ### **Cara Menggunakan**
    #### **1. Masukkan Parameter Cuaca:**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **A. Curah Hujan:**
        - Masukkan nilai 0.00 sampai 500.00 mm
        - Contoh: 100.00 mm untuk hujan sedang
        """)
        
        st.markdown("""
        **B. Tinggi Air:**
        - Masukkan nilai 60.00 sampai 150.00 mdpl
        - Contoh: 100.00 mdpl untuk level normal
        """)
    
    with col2:
        st.markdown("""
        **C. Kelembapan:**
        - Masukkan nilai 0.00 sampai 100.00%
        - Contoh: 70.00% untuk kondisi lembap
        """)
        
        st.markdown("""
        **D. Suhu Harian:**
        - Suhu Minimum: -50.0 sampai 50.0°C
        - Suhu Maksimum: -50.0 sampai 50.0°C
        - Pastikan maksimum ≥ minimum
        - Sistem menghitung rata-rata otomatis
        """)
    
    st.markdown("""
    #### **2. Lakukan Prediksi:**
    - Klik tombol **"PREDIKSI SEKARANG"**
    - Tunggu proses analisis (1-2 detik)
    - Lihat hasil prediksi
    """)
    
    st.markdown("""
    #### **3. Baca Hasil Prediksi:**
    
    **Status Risiko:**
    - **RENDAH:** Warna hijau, kondisi aman
    - **MENENGAH:** Warna kuning, perlu waspada
    - **TINGGI:** Warna merah, potensi banjir
    
    **Informasi Tambahan:**
    - Risk Level: Nilai 0.000 sampai 1.000
    - Pesan rekomendasi: Saran tindakan
    - Progress bar: Visualisasi tingkat risiko
    """)
    
    st.markdown("""
    #### **4. Detail Parameter (Opsional):**
    - Klik "DETAIL PARAMETER INPUT"
    - Lihat interpretasi masing-masing parameter
    - Peringatan jika parameter di luar normal
    """)
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    ### **Tips Penggunaan**
    1. **Untuk skenario normal:** Gunakan nilai default
    2. **Untuk skenario hujan lebat:** Tingkatkan curah hujan >150 mm
    3. **Untuk testing ekstrem:** Coba kombinasi parameter maksimal
    4. **Reset parameter:** Klik "Uji Parameter Lain"
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Contoh Skenario**
    
    | Kondisi | Curah Hujan | Tinggi Air | Hasil |
    |---------|-------------|------------|-------|
    | **Aman** | 50 mm | 90 mdpl | **RENDAH** |
    | **Waspada** | 150 mm | 120 mdpl | **MENENGAH** |
    | **Bahaya** | 250 mm | 140 mdpl | **TINGGI** |
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 6. PANDUAN UMUM ====================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="panduan-umum"> 6. PANDUAN UMUM PENGGUNAAN</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Alur Kerja Rekomendasi**
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### **Untuk Masyarakat Umum:**
        1. Pantau **Prediksi Real-time** untuk kondisi terkini
        2. Jika melihat banjir, laporkan di **Lapor Banjir**
        3. Gunakan **Simulasi Banjir** untuk memahami parameter
        """)
    
    with col2:
        st.markdown("""
        #### **Untuk Petugas/Relawan:**
        1. Pantau **Prediksi Real-time** setiap hari
        2. Cek **Catatan Laporan** untuk informasi lapangan
        3. Analisis tren di **Statistik 1 Tahun**
        """)
    
    st.markdown("""
    ### **Tips Penting**
    1. **Refresh Halaman:** Jika data tidak update, refresh browser
    2. **Waktu Operasional:** Sistem berjalan 24/7
    3. **Validasi Data:** Pastikan data yang dimasukkan akurat
    4. **Konsultasi:** Gunakan informasi sebagai referensi, bukan pengganti ahli
    """)
    
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    ### **Troubleshooting**
    
    **1. Form tidak bisa dikirim:**
    - Pastikan semua field wajib terisi
    - Pastikan foto diunggah
    - Cek koneksi internet
    
    **2. Data tidak muncul:**
    - Refresh halaman
    - Tunggu beberapa saat
    - Cek koneksi internet
    
    **3. Prediksi tidak akurat:**
    - Pastikan parameter dimasukkan dengan benar
    - Gunakan nilai dalam rentang yang ditentukan
    - Hubungi admin jika masalah berlanjut
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== 7. DUKUNGAN TEKNIS ====================
    st.markdown('<div class="contact-box">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title" id="dukungan-teknis"> 7. DUKUNGAN TEKNIS</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### **Jika mengalami kesulitan:**
    1. **Baca panduan ini** dengan seksama
    2. **Periksa koneksi internet** Anda
    3. **Coba refresh** halaman
    4. **Hubungi kontak** di sidebar kiri
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### **📧 Email**
        tyarawahyusaputra@gmail.com
        """)
    
    with col2:
        st.markdown("""
        ### **📱 Telepon**
        085156959561
        """)
    
    with col3:
        st.markdown("""
        ### **📍 Lokasi**
        Jl. Diponegoro No. 52-58
        Salatiga, Jawa Tengah
        """)
    
    st.markdown("---")
    
    st.warning("""
    **CATATAN PENTING:**  
    Sistem ini adalah alat bantu untuk pemantauan dan prediksi banjir.  
    Selalu ikuti arahan dari pihak berwenang dan prioritaskan keselamatan diri.  
    Informasi dari sistem ini harus digunakan sebagai referensi tambahan, bukan satu-satunya sumber keputusan.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("⬆️ Kembali ke Atas", use_container_width=True, type="secondary"):
        st.rerun()