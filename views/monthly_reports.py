import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_monthly_reports_summary(controller):
    """Display monthly reports summary - TERBARU DI ATAS dengan JAM"""
    
    st.markdown("""
    <style>
    .stat-card {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #333333;
    }
    .stat-number {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 5px;
        color: #00a8ff;
    }
    .stat-label {
        font-size: 0.9em;
        color: #aaaaaa;
    }
    
    .report-row {
        padding: 12px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .report-row:last-child {
        border-bottom: none;
    }
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
    .new-badge {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get statistics and reports (sudah terurut dari terbaru)
    stats = controller.get_monthly_statistics()
    reports = controller.get_month_reports()
    
    if not reports:
        st.info(" Tidak ada laporan banjir untuk bulan ini.")
        return
    
    # Daftar laporan dengan informasi urutan dan JAM
    current_month = datetime.now().strftime('%B %Y')
    total_reports = len(reports)
    
    # Filter untuk mendapatkan laporan hari ini
    today = datetime.now().strftime('%Y-%m-%d')
    today_reports = [r for r in reports if r['report_date'] == today]
    
    st.markdown(f"### Daftar Laporan Bulan {current_month}")
    
    # Tampilkan laporan dengan format yang lebih baik
    for i, report in enumerate(reports, 1):
        # Container untuk setiap baris laporan
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
            
            with col1:
                # Alamat dengan badge jika laporan hari ini
                address_text = f"**{i}. {report['address']}**"
                if report['report_date'] == today:
                    st.markdown(address_text, unsafe_allow_html=True)
                
                # Tampilkan waktu dengan badge - PERBAIKAN DI SINI
                time_display = format_time(report['report_time'])
                st.markdown(f'<span class="time-badge"> {time_display}</span>', unsafe_allow_html=True)
            
            with col2:
                st.write(f"**{report['flood_height']}**")
            
            with col3:
                date_display = format_date_full(report['report_date'])
                st.write(date_display)
            
            with col4:
                st.write(report['reporter_name'])
            
            with col5:
                if report['photo_path']:
                    if st.button("Lihat", key=f"view_{i}", use_container_width=True):
                        with st.expander(f"Foto - {report['address']}"):
                            if os.path.exists(report['photo_path']):
                                st.image(report['photo_path'], use_column_width=True)
                            else:
                                st.warning("Foto tidak ditemukan")
                else:
                    st.write("Tidak ada")
        
        # Divider antar laporan (kecuali untuk laporan terakhir)
        if i < total_reports:
            st.divider()

def format_date(date_string):
    """Format date untuk display pendek (dd/mm/yy)"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%y')
    except:
        return date_string

def format_date_full(date_string):
    """Format date untuk display lengkap (Hari, dd/mm/yyyy)"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        return f"{day_name}, {date_obj.strftime('%d/%m/%Y')}"
    except:
        return date_string

def format_time(time_string):
    """Format time untuk display (HH:MM)"""
    try:
        if len(time_string) == 8:  
            return time_string[:5]
        return time_string
    except:
        return time_string
