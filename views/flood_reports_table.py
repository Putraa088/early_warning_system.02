import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show_current_month_reports(controller):
    """Display current month's reports dengan error handling"""
    
    st.markdown("""
    <style>
    .report-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #333333;
    }
    .photo-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .timestamp-badge {
        background: rgba(0, 168, 255, 0.15);
        color: #00a8ff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        reports = controller.get_today_reports()
    except AttributeError as e:
        st.error(f"❌ Error: Controller tidak memiliki method get_today_reports()")
        st.info("⚠️ Silakan periksa kode controller Anda.")
        return
    except Exception as e:
        st.error(f"❌ Error mendapatkan data: {e}")
        return
    
    if not reports:
        st.info(" Tidak ada laporan banjir untuk hari ini.")
        return
    
    st.markdown("---")
    
    st.markdown(f"###  Daftar Laporan Hari Ini ({len(reports)} laporan)")
    
    for i, report in enumerate(reports, 1):
        with st.container():
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            
            with col1:
                address = report.get('Alamat', report.get('alamat', 'N/A'))
                st.write(f"**{i}. {address}**")
                
                timestamp = report.get('Timestamp', '')
                if timestamp:
                    formatted_time = format_timestamp_for_display(timestamp)
                    st.markdown(f'<span class="timestamp-badge"> {formatted_time}</span>', 
                            unsafe_allow_html=True)
                else:
                    time_display = format_time(report.get('report_time', ''))
                    if time_display:
                        st.markdown(f'<span class="timestamp-badge"> {time_display}</span>', 
                                unsafe_allow_html=True)
            
            with col2:
                flood_height = report.get('Tinggi Banjir', report.get('tinggi_banjir', 'N/A'))
                st.write(f"**{flood_height}**")
            
            with col3:
                date_display = format_date(report.get('report_date', ''))
                st.write(date_display)
            
            with col4:
                reporter_name = report.get('Nama Pelapor', report.get('nama_pelapor', 'N/A'))
                st.write(reporter_name)
            
            with col5:
                photo_url = report.get('Photo URL', report.get('photo_url', ''))
                
                if photo_url:
                    if os.path.exists(str(photo_url)):
                        if st.button("Lihat", key=f"view_{i}", use_container_width=True):
                            with st.expander(f"Foto - {address[:30]}...", expanded=True):
                                try:
                                    st.image(photo_url, use_column_width=True)
                                except Exception as e:
                                    st.warning(f"Gagal menampilkan foto: {e}")
                    elif 'drive.google.com' in str(photo_url):
                        if st.button("🔗 Buka", key=f"drive_{i}", use_container_width=True):
                            st.markdown(f"[📎 Buka Foto di Google Drive]({photo_url})")
                    else:
                        st.write("📭 Tidak ada")
                else:
                    st.write("📭 Tidak ada")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if i < len(reports):
            st.divider()
    
    with st.expander(" Analisis Hari Ini", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Laporan", len(reports))
        with col2:
            unique_locations = len(set(
                r.get('Alamat', r.get('alamat', '')) for r in reports
            ))
            st.metric("Lokasi Berbeda", unique_locations)
        with col3:
            unique_reporters = len(set(
                r.get('Nama Pelapor', r.get('nama_pelapor', '')) for r in reports
            ))
            st.metric("Pelapor Berbeda", unique_reporters)

def format_timestamp_for_display(timestamp):
    """Format timestamp untuk display yang konsisten dengan rekapan bulanan"""
    try:
        if not timestamp:
            return ""
        
        if isinstance(timestamp, str):
            formats_to_try = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%d/%m/%Y %H:%M:%S',
                '%d-%m-%Y %H:%M:%S'
            ]
            
            for fmt in formats_to_try:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    break
                except ValueError:
                    continue
            else:
                return timestamp[:16]  
        else:
            dt = timestamp
        
        return dt.strftime('%H:%M')
        
    except Exception:
        if ' ' in str(timestamp):
            parts = str(timestamp).split(' ')
            if len(parts) > 1:
                time_part = parts[1]
                if ':' in time_part:
                    return time_part[:5]  
        return str(timestamp)[:5] if len(str(timestamp)) >= 5 else str(timestamp)

def format_date(date_string):
    """Format date untuk display"""
    try:
        if not date_string:
            return "N/A"
        
        if isinstance(date_string, str):
            try:
                date_obj = datetime.strptime(date_string, '%Y-%m-%d')
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_string, '%d/%m/%Y')
                except ValueError:
                    return str(date_string)
        else:
            date_obj = date_string
        
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        
        return f"{day_name}, {date_obj.strftime('%d/%m/%y')}"
    except:
        return str(date_string) if date_string else "N/A"

def format_time(time_string):
    """Format time untuk display"""
    try:
        if not time_string:
            return ""
        
        if isinstance(time_string, str):
            if ':' in time_string:
                return time_string[:5]  
            return time_string
        else:
            return str(time_string)
    except:
        return str(time_string) if time_string else ""
