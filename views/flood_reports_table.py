import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
from io import BytesIO
from PIL import Image

def show_current_month_reports(controller):
    """Display current month's reports with Base64 photos"""
    
    st.markdown("""
    <style>
    .photo-container {
        border: 1px solid #333;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        background: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get today's reports
    reports = controller.get_today_reports()
    
    if not reports:
        st.info(" Tidak ada laporan banjir untuk hari ini.")
        return
    
    st.markdown("---")
    
    # Header
    st.markdown(f"###  Daftar Laporan Hari Ini ({len(reports)} laporan)")
    
    # Display reports
    for i, report in enumerate(reports, 1):
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 2])
        
        with col1:
            st.write(f"**{i}. {report['address']}**")
            if 'timestamp' in report:
                st.caption(f"ID: {report['id']} | {report['timestamp'][11:19]}")
        
        with col2:
            st.write(f"**{report['flood_height']}**")
        
        with col3:
            date_display = format_date(report.get('report_date', ''))
            st.write(date_display)
        
        with col4:
            time_display = report.get('report_time', '')[:5] if report.get('report_time') and len(report.get('report_time', '')) >= 5 else "N/A"
            st.write(time_display)
        
        with col5:
            st.write(report['reporter_name'])
        
        with col6:
            # Check for Base64 photo
            if report.get('photo_base64') and len(report['photo_base64']) > 100:
                if st.button(" Lihat Foto", key=f"view_base64_{report['id']}", use_container_width=True):
                    # Decode and display Base64
                    display_base64_photo(report['photo_base64'], report['address'])
            else:
                st.write(" Tidak ada")
        
        if i < len(reports):
            st.divider()

def display_base64_photo(base64_string, address):
    """Display photo from Base64 string"""
    try:
        # Check if truncated
        if base64_string.endswith('...[TRUNCATED]'):
            st.warning("⚠️ Foto terlalu besar, hanya preview tersedia")
            base64_string = base64_string.replace('...[TRUNCATED]', '')
        
        # Decode Base64
        image_data = base64.b64decode(base64_string)
        
        # Create BytesIO object
        image_bytes = BytesIO(image_data)
        
        # Open image
        image = Image.open(image_bytes)
        
        # Display with caption
        st.markdown(f"###  Foto: {address}")
        st.image(image, use_column_width=True, caption=f"Laporan dari: {address}")
        
        # Show image info
        st.caption(f"Format: {image.format} | Size: {image.size} | Mode: {image.mode}")
        
    except Exception as e:
        st.error(f"❌ Gagal menampilkan foto: {str(e)}")
        st.info("Coba lihat foto dari file lokal jika tersedia")
        
        # Try to show from local path as fallback
        if os.path.exists('uploads'):
            st.write("📁 Isi folder uploads:")
            files = os.listdir('uploads')
            for file in files[:5]:  # Show first 5 files
                st.write(f"  - {file}")

def format_date(date_string):
    """Format date untuk display"""
    try:
        if not date_string:
            return "N/A"
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        return f"{day_name}, {date_obj.strftime('%d/%m/%y')}"
    except:
        return date_string
