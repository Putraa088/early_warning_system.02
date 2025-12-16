import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

def show_monthly_reports_summary(controller):
    """Display monthly reports summary with Base64 photos"""
    
    st.markdown("""
    <style>
    .time-badge {
        background: rgba(0, 168, 255, 0.15);
        color: #00a8ff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
    }
    .photo-preview {
        max-width: 100px;
        max-height: 100px;
        border-radius: 8px;
        border: 2px solid #333;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .photo-preview:hover {
        transform: scale(1.05);
        border-color: #00a8ff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get reports
    reports = controller.get_month_reports()
    
    if not reports:
        st.info(" Tidak ada laporan banjir untuk bulan ini.")
        return
    
    # Statistics
    current_month = datetime.now().strftime('%B %Y')
    total_reports = len(reports)
    
    # Count reports with photos
    reports_with_photos = sum(1 for r in reports if r.get('photo_base64') and len(r['photo_base64']) > 100)
    
    # Filter untuk mendapatkan laporan hari ini
    today = datetime.now().strftime('%Y-%m-%d')
    today_reports = [r for r in reports if r['report_date'] == today]
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laporan", total_reports)
    with col2:
        st.metric("Dengan Foto", reports_with_photos)
    with col3:
        st.metric("Laporan Hari Ini", len(today_reports))
    with col4:
        unique_reporters = len(set(r['reporter_name'] for r in reports))
        st.metric("Jumlah Pelapor", unique_reporters)
    
    st.markdown("---")
    
    st.markdown(f"###  Daftar Laporan Bulan {current_month}")
    
    # Tampilkan laporan dengan thumbnail
    for i, report in enumerate(reports, 1):
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 1, 2])
            
            with col1:
                # Alamat dengan badge jika laporan hari ini
                address_text = f"**{i}. {report['address']}**"
                if report['report_date'] == today:
                    st.markdown(f"{address_text} 🆕", unsafe_allow_html=True)
                else:
                    st.markdown(address_text, unsafe_allow_html=True)
                
                # Waktu
                time_display = format_time(report.get('report_time', ''))
                if time_display:
                    st.markdown(f'<span class="time-badge">🕐 {time_display}</span>', unsafe_allow_html=True)
            
            with col2:
                st.write(f"**{report['flood_height']}**")
            
            with col3:
                date_display = format_date_full(report.get('report_date', ''))
                st.write(date_display)
            
            with col4:
                st.write(report['reporter_name'])
            
            with col5:
                # Show photo thumbnail if available
                if report.get('photo_base64') and len(report['photo_base64']) > 100:
                    try:
                        # Create thumbnail from Base64
                        image_data = base64.b64decode(report['photo_base64'][:10000])  # First part only for thumbnail
                        image = Image.open(BytesIO(image_data))
                        
                        # Resize for thumbnail
                        image.thumbnail((100, 100))
                        
                        # Display clickable thumbnail
                        if st.button("👁️", key=f"thumb_{report['id']}", help="Klik untuk lihat foto penuh"):
                            display_full_photo_base64(report['photo_base64'], report['address'])
                    except:
                        st.write("📷")
                else:
                    st.write("📭")
            
            with col6:
                # Action buttons
                if st.button("📋 Detail", key=f"detail_{report['id']}", use_container_width=True):
                    show_report_details(report)
        
        # Divider antar laporan
        if i < total_reports:
            st.divider()

def display_full_photo_base64(base64_string, address):
    """Display full photo from Base64 in an expander"""
    with st.expander(f"📸 Foto Lengkap: {address}", expanded=True):
        try:
            # Check if truncated
            if base64_string.endswith('...[TRUNCATED]'):
                st.warning("⚠️ Foto terlalu besar, hanya preview tersedia di Google Sheets")
                base64_string = base64_string.replace('...[TRUNCATED]', '')
            
            # Decode Base64
            image_data = base64.b64decode(base64_string)
            
            # Create BytesIO object
            image_bytes = BytesIO(image_data)
            
            # Open image
            image = Image.open(image_bytes)
            
            # Display
            st.image(image, use_column_width=True, caption=f"Laporan dari: {address}")
            
            # Image info
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ukuran File", f"{len(image_data):,} bytes")
            with col2:
                st.metric("Dimensi", f"{image.size[0]}x{image.size[1]}")
            
        except Exception as e:
            st.error(f"❌ Gagal menampilkan foto: {str(e)}")

def show_report_details(report):
    """Show detailed report information"""
    with st.expander(f"📋 Detail Laporan: {report['address']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📝 Informasi Laporan**")
            st.write(f"Alamat: {report['address']}")
            st.write(f"Tinggi Banjir: {report['flood_height']}")
            st.write(f"Tanggal: {report['report_date']}")
            st.write(f"Waktu: {report['report_time']}")
        
        with col2:
            st.write("**👤 Informasi Pelapor**")
            st.write(f"Nama: {report['reporter_name']}")
            if report['reporter_phone']:
                st.write(f"Telepon: {report['reporter_phone']}")
            st.write(f"IP Address: {report.get('ip_address', 'N/A')}")
        
        # Show photo if available
        if report.get('photo_base64') and len(report['photo_base64']) > 100:
            st.write("---")
            st.write("** Foto Laporan**")
            display_full_photo_base64(report['photo_base64'], report['address'])

def format_date_full(date_string):
    """Format date untuk display lengkap"""
    try:
        if not date_string:
            return "N/A"
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        return f"{day_name}, {date_obj.strftime('%d/%m/%Y')}"
    except:
        return date_string

def format_time(time_string):
    """Format time untuk display"""
    try:
        if time_string and len(time_string) >= 5:
            return time_string[:5]
        return ""
    except:
        return ""
