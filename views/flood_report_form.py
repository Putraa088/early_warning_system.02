import streamlit as st

def show_flood_report_form(controller):
    """Show flood report form - TIDAK ADA PERUBAHAN"""
    
    with st.form("flood_report_form"):
        st.markdown("### Formulir Laporan Banjir")
        
        # Form fields - TANPA PERUBAHAN
        address = st.text_area(
            "Lokasi Kejadian*",
            placeholder="Contoh: Jl. Diponegoro No. 52, Salatiga, Jawa Tengah",
            help="Sebutkan lokasi kejadian banjir dengan jelas"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            flood_height = st.number_input(
                "Tinggi Banjir (cm)*",
                min_value=0.0,
                max_value=500.0,
                step=0.1,
                help="Tinggi genangan air dalam centimeter"
            )
        
        with col2:
            reporter_name = st.text_input(
                "Nama Pelapor*",
                placeholder="Nama lengkap pelapor",
                help="Nama Anda sebagai pelapor"
            )
        
        reporter_phone = st.text_input(
            "Nomor Telepon (Opsional)",
            placeholder="081234567890",
            help="Nomor telepon untuk konfirmasi"
        )
        
        photo_file = st.file_uploader(
            "Foto Kejadian (Opsional)",
            type=['jpg', 'jpeg', 'png', 'gif'],
            help="Upload foto kejadian banjir jika ada"
        )
        
        if photo_file:
            st.image(photo_file, caption="Pratinjau Foto", width=300)
        
        # Terms and conditions
        st.markdown("---")
        agreed = st.checkbox(
            "Saya menyetujui bahwa data yang saya berikan adalah benar dan dapat dipertanggungjawabkan*"
        )
        
        # Submit button
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submitted = st.form_submit_button(
                "📤 KIRIM LAPORAN",
                use_container_width=True,
                type="primary",
                disabled=not agreed
            )
        
        if submitted:
            if not address or not reporter_name or flood_height <= 0:
                st.error("❌ Harap isi semua field yang wajib diisi (*)")
            else:
                with st.spinner("Mengirim laporan..."):
                    success, message = controller.submit_report(
                        address=address,
                        flood_height=flood_height,
                        reporter_name=reporter_name,
                        reporter_phone=reporter_phone,
                        photo_file=photo_file
                    )
                    
                    if success:
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)
