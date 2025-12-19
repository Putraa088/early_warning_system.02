import streamlit as st
import pandas as pd
import os
from datetime import datetime
import pytz

def show_monthly_reports_summary(controller):
    """Display monthly reports summary dengan struktur baru"""
    
    st.markdown("""
    <style>
    .monthly-report-card {
        background: linear-gradient(145deg, #1a1a1a, #222222);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #333333;
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
    .photo-preview {
        max-width: 150px;
        border-radius: 8px;
        border: 2px solid #333;
    }
    .new-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get reports dari controller
    try:
        reports = controller.get_month_reports()
    except AttributeError as e:
        st.error(f"❌ Error: {e}")
        st.info("⚠️ Controller tidak memiliki method get_month_reports()")
        return
    
    if not reports:
        st.info("📭 Tidak ada laporan banjir untuk bulan ini.")
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: rgba(255,255,255,0.03); border-radius: 10px;">
            <h3 style="color: #666;">Belum ada data laporan</h3>
            <p style="color: #888;">Silakan buka halaman "Lapor Banjir" untuk membuat laporan pertama Anda.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Daftar laporan
    current_month = datetime.now().strftime('%B %Y')
    total_reports = len(reports)
    
    # Filter untuk mendapatkan laporan hari ini
    today = datetime.now().strftime('%Y-%m-%d')
    today_reports = [r for r in reports if r.get('report_date') == today]
    
    # ============ STATISTICS CARDS ============
    st.markdown("### 📊 Statistik Bulanan")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laporan", total_reports)
    with col2:
        st.metric("Laporan Hari Ini", len(today_reports))
    with col3:
        # ✅ Gunakan 'Nama Pelapor' bukan 'reporter_name'
        unique_reporters = len(set(r.get('Nama Pelapor', r.get('nama_pelapor', '')) for r in reports))
        st.metric("Jumlah Pelapor", unique_reporters)
    with col4:
        # ✅ Gunakan 'Alamat' bukan 'address'
        locations = len(set(r.get('Alamat', r.get('alamat', '')) for r in reports))
        st.metric("Lokasi Berbeda", locations)
    
    st.markdown("---")
    
    # ============ MONTHLY SUMMARY ============
    st.markdown(f"### 📋 Daftar Laporan Bulan {current_month}")
    st.caption(f"Menampilkan {len(reports)} laporan terbaru")
    
    # Search and filter
    with st.expander("🔍 Filter Pencarian", expanded=False):
        col_search1, col_search2 = st.columns(2)
        
        with col_search1:
            search_address = st.text_input("Cari berdasarkan alamat:", "")
        
        with col_search2:
            search_reporter = st.text_input("Cari berdasarkan nama pelapor:", "")
        
        # Filter reports based on search
        filtered_reports = reports
        if search_address:
            filtered_reports = [r for r in filtered_reports if search_address.lower() in str(r.get('Alamat', r.get('alamat', ''))).lower()]
        if search_reporter:
            filtered_reports = [r for r in filtered_reports if search_reporter.lower() in str(r.get('Nama Pelapor', r.get('nama_pelapor', ''))).lower()]
        
        if len(filtered_reports) != len(reports):
            st.info(f"🔍 Menampilkan {len(filtered_reports)} dari {len(reports)} laporan")
            reports = filtered_reports
    
    # Display reports
    for i, report in enumerate(reports, 1):
        with st.container():
            st.markdown('<div class="monthly-report-card">', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
            
            with col1:
                # Address with new badge if today
                address = report.get('Alamat', report.get('alamat', 'N/A'))
                reporter_name = report.get('Nama Pelapor', report.get('nama_pelapor', 'N/A'))
                
                address_text = f"**{i}. {address}**"
                if report.get('report_date') == today:
                    st.markdown(f"{address_text} <span class='new-badge'>BARU</span>", unsafe_allow_html=True)
                else:
                    st.markdown(address_text, unsafe_allow_html=True)
                
                # Reporter info
                st.caption(f"👤 {reporter_name}")
                
                # Waktu (sudah WIB)
                time_display = format_time(report.get('report_time', ''))
                if time_display:
                    st.markdown(f'<span class="time-badge">🕐 {time_display}</span>', unsafe_allow_html=True)
            
            with col2:
                # Flood height
                flood_height = report.get('Tinggi Banjir', report.get('tinggi_banjir', 'N/A'))
                st.write(f"**{flood_height}**")
                
                # Status
                status = report.get('Status', 'pending')
                if status == 'verified':
                    st.success("✅ Diverifikasi")
                elif status == 'pending':
                    st.warning("⏳ Menunggu")
                else:
                    st.info(status)
            
            with col3:
                # Date
                date_display = format_date_full(report.get('report_date', ''))
                st.write(date_display)
                
                # ID
                report_id = report.get('id', 'N/A')
                st.caption(f"ID: {report_id}")
            
            with col4:
                # Contact info
                phone = report.get('No HP', report.get('no_hp', ''))
                if phone:
                    st.write(f"📞 {phone}")
                else:
                    st.write("📞 -")
                
                # IP Address
                ip = report.get('IP Address', report.get('ip_address', ''))
                if ip:
                    st.caption(f"🌐 {ip}")
            
            with col5:
                # Photo preview
                photo_url = report.get('Photo URL', report.get('photo_url', ''))
                
                if photo_url:
                    # Check if it's a Google Drive URL
                    if 'drive.google.com' in str(photo_url):
                        # Extract file ID for thumbnail
                        try:
                            if 'id=' in photo_url:
                                file_id = photo_url.split('id=')[-1]
                                thumbnail_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w150"
                                
                                if st.button("👁️", key=f"view_{report_id}", help="Lihat foto", use_container_width=True):
                                    with st.expander(f"📷 Foto - {address[:30]}...", expanded=True):
                                        st.markdown(f"[📎 Buka di Google Drive]({photo_url})")
                                        try:
                                            st.image(thumbnail_url, use_column_width=True)
                                        except:
                                            st.warning("Gagal menampilkan thumbnail")
                            else:
                                if st.button("🔗", key=f"link_{report_id}", help="Buka link foto", use_container_width=True):
                                    st.markdown(f"[📎 Buka Foto]({photo_url})")
                        except:
                            if st.button("🔗", key=f"link_{report_id}_2", help="Buka link foto", use_container_width=True):
                                st.markdown(f"[📎 Buka Foto]({photo_url})")
                    
                    # Local file
                    elif os.path.exists(str(photo_url)):
                        if st.button("👁️", key=f"local_{report_id}", help="Lihat foto", use_container_width=True):
                            with st.expander(f"📷 Foto - {address[:30]}...", expanded=True):
                                try:
                                    st.image(photo_url, use_column_width=True)
                                except:
                                    st.warning("Foto tidak dapat ditampilkan")
                    else:
                        st.write("📭")
                else:
                    st.write("📭")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider antar laporan
        if i < len(reports):
            st.markdown('<div style="height: 1px; background: rgba(255,255,255,0.1); margin: 10px 0;"></div>', unsafe_allow_html=True)
    
    # ============ EXPORT OPTIONS ============
    st.markdown("---")
    
    with st.expander("📤 Export Data", expanded=False):
        col_export1, col_export2, col_export3 = st.columns(3)
        
        with col_export1:
            if st.button("📊 Export ke CSV", use_container_width=True):
                try:
                    # Prepare data for CSV
                    export_data = []
                    for report in reports:
                        export_data.append({
                            'ID': report.get('id', ''),
                            'Tanggal': report.get('report_date', ''),
                            'Waktu': report.get('report_time', ''),
                            'Alamat': report.get('Alamat', report.get('alamat', '')),
                            'Tinggi_Banjir': report.get('Tinggi Banjir', report.get('tinggi_banjir', '')),
                            'Nama_Pelapor': report.get('Nama Pelapor', report.get('nama_pelapor', '')),
                            'No_HP': report.get('No HP', report.get('no_hp', '')),
                            'Status': report.get('Status', 'pending')
                        })
                    
                    df = pd.DataFrame(export_data)
                    csv = df.to_csv(index=False, encoding='utf-8')
                    
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"laporan_banjir_{current_month.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error exporting: {e}")
        
        with col_export2:
            if st.button("📋 Salin Ringkasan", use_container_width=True):
                summary = f"""
                Ringkasan Laporan Banjir {current_month}
                --------------------------------
                Total Laporan: {total_reports}
                Laporan Hari Ini: {len(today_reports)}
                Jumlah Pelapor: {unique_reporters}
                Lokasi Berbeda: {locations}
                
                Laporan terbaru:
                """
                for i, report in enumerate(reports[:5], 1):
                    summary += f"\n{i}. {report.get('Alamat', report.get('alamat', ''))} - {report.get('Nama Pelapor', report.get('nama_pelapor', ''))}"
                
                st.code(summary)
                st.success("Ringkasan siap disalin!")
        
        with col_export3:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()

def format_date_full(date_string):
    """Format date untuk display lengkap"""
    try:
        if not date_string:
            return "N/A"
        
        # Parse date string
        if isinstance(date_string, str):
            date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        else:
            date_obj = date_string
        
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        day_name = days[date_obj.weekday()]
        
        months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        month_name = months[date_obj.month - 1]
        
        return f"{day_name}, {date_obj.day} {month_name} {date_obj.year}"
    except:
        return str(date_string) if date_string else "N/A"

def format_time(time_string):
    """Format time untuk display (sudah WIB, tidak perlu konversi)"""
    try:
        if not time_string:
            return ""
        
        if isinstance(time_string, str):
            # Handle different time formats
            if ':' in time_string:
                parts = time_string.split(':')
                if len(parts) >= 2:
                    return f"{parts[0]}:{parts[1]}"
            return time_string[:5] if len(time_string) >= 5 else time_string
        else:
            return str(time_string)
    except:
        return str(time_string) if time_string else ""

def format_report_date(report):
    """Format report date and time untuk display"""
    try:
        date_str = report.get('report_date', '')
        time_str = report.get('report_time', '')
        
        date_display = format_date_full(date_str)
        time_display = format_time(time_str)
        
        if date_display and time_display:
            return f"{date_display} - {time_display}"
        elif date_display:
            return date_display
        elif time_display:
            return time_display
        else:
            return "N/A"
    except:
        return "N/A"

# Function untuk compatibility dengan kode lama
def show_monthly_reports(controller):
    """Alias untuk compatibility"""
    return show_monthly_reports_summary(controller)
