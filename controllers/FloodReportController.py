from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
import os
import uuid
from datetime import datetime
import streamlit as st
import traceback
import sqlite3
from datetime import timedelta

class FloodReportController:
    def __init__(self):
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        self.upload_folder = "uploads"
        
        try:
            self.sheets_model = GoogleSheetsModel()
            if self.sheets_model and hasattr(self.sheets_model, 'client') and self.sheets_model.client:
                print("✅ Google Sheets connected for flood reports")
            else:
                print("⚠️ Google Sheets offline - using SQLite only")
                self.sheets_model = None
        except Exception as e:
            print(f"⚠️ Google Sheets init error: {e}")
            self.sheets_model = None
        
        self._ensure_upload_folder()
        print("✅ FloodReportController initialized")
    
    def _ensure_upload_folder(self):
        """Ensure upload folder exists"""
        try:
            if not os.path.exists(self.upload_folder):
                os.makedirs(self.upload_folder)
                print(f"✅ Created upload folder: {os.path.abspath(self.upload_folder)}")
            else:
                print(f"✅ Upload folder exists: {self.upload_folder}")
        except Exception as e:
            print(f"❌ Error creating upload folder: {e}")
    
    def check_daily_limit(self, ip_address):
        """Check if daily limit (10 reports per IP) has been reached"""
        try:
            today_count = self.flood_model.get_today_reports_count_by_ip(ip_address)
            can_submit = today_count < 10
            print(f"📊 Daily limit check: IP={ip_address}, Count={today_count}, CanSubmit={can_submit}")
            return can_submit
        except Exception as e:
            print(f"⚠️ Error in check_daily_limit: {e}")
            return True
    
    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report"""
        photo_url = None
        photo_filename = None
        
        try:
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            if not self.check_daily_limit(client_ip):
                return False, "❌ Mohon maaf batas laporan harian telah mencapai batas, silahkan kembali lagi besok."
            
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
                    
                    if file_extension not in valid_extensions:
                        return False, f"❌ Format file tidak didukung. Gunakan: {', '.join(valid_extensions)}"
                    
                    photo_filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_path = os.path.join(self.upload_folder, photo_filename)
                    
                    print(f"📸 Saving photo to: {photo_path}")
                    
                    with open(photo_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    photo_url = photo_path
                    print(f"✅ Photo saved: {photo_filename}")
                    
                except Exception as e:
                    print(f"⚠️ Error saving photo: {e}")
                    photo_url = None
                    photo_filename = None
            
            report_id = self.flood_model.create_report(
                alamat=address,  
                tinggi_banjir=flood_height,  
                nama_pelapor=reporter_name,  
                no_hp=reporter_phone,  
                photo_url=photo_url,  
                ip_address=client_ip  
            )
            
            if not report_id:
                print("❌ Failed to save to SQLite")
                if photo_url and os.path.exists(photo_url):
                    try:
                        os.remove(photo_url)
                    except:
                        pass
                return False, "❌ Gagal menyimpan laporan ke database lokal."
            
            if self.sheets_model and self.sheets_model.client:
                try:
                    print("📊 Saving to Google Sheets...")
                    
                    sheets_data = {
                        'address': str(address),
                        'flood_height': str(flood_height),
                        'reporter_name': str(reporter_name),
                        'reporter_phone': str(reporter_phone) if reporter_phone else '',
                        'ip_address': str(client_ip),
                        'photo_url': photo_url if photo_url else ''
                    }
                    
                    print(f"📋 Google Sheets data prepared")
                    
                    success = self.sheets_model.save_flood_report(sheets_data)
                    if success:
                        print("✅ Report saved to Google Sheets")
                        gs_status = " (dan Google Sheets)"
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                        gs_status = " (Google Sheets gagal)"
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
                    gs_status = " (Google Sheets error)"
            else:
                print("ℹ️ Google Sheets not available")
                gs_status = ""
            
            today_reports = self.flood_model.get_today_reports()
            print(f"✅ Verification: Total reports today = {len(today_reports)}")
            
            return True, f"✅ Informasi anda telah terkirim! Terimakasih atas laporannya."
                
        except Exception as e:
            print(f"❌ CRITICAL Error in submit_report: {e}")
            traceback.print_exc()
            
            if photo_url and os.path.exists(photo_url):
                try:
                    os.remove(photo_url)
                except:
                    pass
            
            return False, f"❌ Error sistem: {str(e)}"
    
    # ============ FUNGSI OTOMATIS TANPA MANUAL INPUT ============
    
    def get_today_reports(self):
        """Get today's flood reports - OTOMATIS"""
        try:
            if self.sheets_model and self.sheets_model.client:
                return self._get_filtered_reports_from_gsheets('today')
            else:
                return self.flood_model.get_today_reports()
        except Exception as e:
            print(f"⚠️ Error in get_today_reports: {e}")
            return self.flood_model.get_today_reports()
    
    def get_month_reports(self):
        """Get this month's flood reports - OTOMATIS"""
        try:
            if self.sheets_model and self.sheets_model.client:
                return self._get_filtered_reports_from_gsheets('month')
            else:
                return self.flood_model.get_month_reports()
        except Exception as e:
            print(f"⚠️ Error in get_month_reports: {e}")
            return self.flood_model.get_month_reports()
    
    def get_all_reports(self):
        """Get all flood reports - OTOMATIS"""
        try:
            if self.sheets_model and self.sheets_model.client:
                return self._get_filtered_reports_from_gsheets('all')
            else:
                return self.flood_model.get_all_reports()
        except Exception as e:
            print(f"⚠️ Error in get_all_reports: {e}")
            return self.flood_model.get_all_reports()
    
    def get_monthly_statistics(self):
        """Get monthly statistics for reports"""
        return self.flood_model.get_monthly_statistics()
    
    def get_yearly_statistics(self):
        """Get yearly statistics - OTOMATIS"""
        try:
            if self.sheets_model and self.sheets_model.client:
                return self._get_yearly_stats_auto()
            else:
                return self._get_yearly_stats_from_sqlite()
        except Exception as e:
            print(f"❌ Error in get_yearly_statistics: {e}")
            return self._get_empty_yearly_stats()
    
    # ============ CORE AUTOMATIC FUNCTIONS ============
    
    def _get_filtered_reports_from_gsheets(self, filter_type='all'):
        """Get filtered reports from Google Sheets - FULLY AUTOMATIC"""
        try:
            if not self.sheets_model or not self.sheets_model.client:
                print("⚠️ Google Sheets offline")
                return []
            
            print(f"📊 Getting {filter_type} reports from Google Sheets...")
            
            worksheet = self.sheets_model.worksheet
            all_records = worksheet.get_all_records()
            
            if not all_records:
                print("⚠️ No records in Google Sheets")
                return []
            
            current_date = datetime.now()
            filtered_reports = []
            
            for i, record in enumerate(all_records):
                timestamp = record.get('Timestamp', '')
                if not timestamp:
                    continue
                
                timestamp_str = str(timestamp).strip()
                
                # OTOMATIS DETECT apakah data termasuk dalam filter
                include_record = False
                
                if filter_type == 'all':
                    include_record = True
                
                elif filter_type == 'month':
                    # Cari data dengan bulan yang sama (tahun berapapun)
                    current_month = current_date.strftime("%m")  # "12"
                    
                    # Cek berbagai format
                    if f"-{current_month}-" in timestamp_str:  # "2025-12-20"
                        include_record = True
                    elif f"/{current_month}/" in timestamp_str:  # "20/12/2025"
                        include_record = True
                    elif current_date.strftime("%b") in timestamp_str:  # "Dec"
                        include_record = True
                
                elif filter_type == 'today':
                    # Cari data dengan tanggal hari ini
                    today_str = current_date.strftime("%Y-%m-%d")
                    
                    if today_str in timestamp_str:  # "2025-12-20"
                        include_record = True
                    else:
                        # Coba format lain: "20/12/2025"
                        today_parts = today_str.split('-')
                        today_alt = f"{today_parts[2]}/{today_parts[1]}/{today_parts[0]}"
                        if today_alt in timestamp_str:
                            include_record = True
                
                if include_record:
                    # Format data secara konsisten
                    filtered_reports.append({
                        'id': i + 1,
                        'Alamat': record.get('Alamat', ''),
                        'Tinggi Banjir': record.get('Tinggi Banjir', ''),
                        'Nama Pelapor': record.get('Nama Pelapor', ''),
                        'No HP': record.get('No HP', ''),
                        'IP Address': record.get('IP Address', ''),
                        'Photo URL': record.get('Photo URL', ''),
                        'Status': record.get('Status', 'pending'),
                        'Timestamp': timestamp_str,
                        'report_date': self._extract_date_from_timestamp(timestamp_str),
                        'report_time': self._extract_time_from_timestamp(timestamp_str)
                    })
            
            # Sort by timestamp descending
            filtered_reports.sort(key=lambda x: x.get('Timestamp', ''), reverse=True)
            
            print(f"✅ Found {len(filtered_reports)} {filter_type} reports")
            return filtered_reports
            
        except Exception as e:
            print(f"❌ Error getting {filter_type} reports: {e}")
            traceback.print_exc()
            
            # Fallback ke SQLite
            if filter_type == 'today':
                return self.flood_model.get_today_reports()
            elif filter_type == 'month':
                return self.flood_model.get_month_reports()
            else:
                return self.flood_model.get_all_reports()
    
    def _extract_date_from_timestamp(self, timestamp_str):
        """Extract date from timestamp string automatically"""
        try:
            # Coba berbagai format
            if '-' in timestamp_str and len(timestamp_str) >= 10:
                return timestamp_str[:10]  # "2025-12-20"
            elif '/' in timestamp_str:
                parts = timestamp_str.split('/')
                if len(parts) >= 3:
                    return f"{parts[2]}-{parts[1]}-{parts[0]}"  # "20/12/2025" → "2025-12-20"
            return timestamp_str[:10] if len(timestamp_str) >= 10 else ''
        except:
            return ''
    
    def _extract_time_from_timestamp(self, timestamp_str):
        """Extract time from timestamp string automatically"""
        try:
            if len(timestamp_str) > 10 and ' ' in timestamp_str:
                time_part = timestamp_str.split(' ')[1]
                if ':' in time_part:
                    return time_part[:8]  # "10:43:24"
            return timestamp_str[11:19] if len(timestamp_str) > 10 else ''
        except:
            return ''
    
    def _get_yearly_stats_auto(self):
        """Get yearly statistics - FULLY AUTOMATIC"""
        try:
            from datetime import datetime
            
            if not self.sheets_model or not self.sheets_model.client:
                return self._get_yearly_stats_from_sqlite()
            
            worksheet = self.sheets_model.worksheet
            all_records = worksheet.get_all_records()
            
            if not all_records:
                return self._get_empty_yearly_stats()
            
            # OTOMATIS GROUP BY BULAN dari data yang ada
            month_counts = {}
            
            for record in all_records:
                timestamp = record.get('Timestamp', '')
                if not timestamp:
                    continue
                
                # OTOMATIS extract bulan dari timestamp
                month_key = self._extract_month_from_timestamp(str(timestamp))
                if month_key:
                    month_counts[month_key] = month_counts.get(month_key, 0) + 1
            
            # Buat data untuk 12 bulan terakhir OTOMATIS
            current_date = datetime.now()
            months_data = []
            
            # Dapatkan tahun dari data yang ada (ambil yang paling banyak)
            data_year = self._detect_year_from_data(all_records) or current_date.year
            
            for i in range(11, -1, -1):
                target_date = current_date - timedelta(days=30*i)
                year_month = target_date.strftime('%Y-%m')
                month_name = target_date.strftime('%b')
                month_num = target_date.strftime('%m')
                
                # Cari data untuk bulan ini
                month_key = f"{data_year}-{month_num}" if data_year else month_num
                report_count = month_counts.get(month_key, 0)
                
                # Jika tidak ada data untuk key lengkap, coba hanya bulan
                if report_count == 0 and month_num in month_counts:
                    report_count = month_counts[month_num]
                
                is_current = (month_num == current_date.strftime('%m'))
                
                months_data.append({
                    'year_month': year_month,
                    'month_name': month_name,
                    'report_count': report_count,
                    'is_current': is_current
                })
            
            # Hitung statistik
            report_counts = [item['report_count'] for item in months_data]
            total_reports = sum(report_counts)
            avg_per_month = total_reports / len(months_data) if months_data else 0
            
            if months_data and any(report_counts):
                max_item = max(months_data, key=lambda x: x['report_count'])
                max_month = max_item['month_name']
                max_count = max_item['report_count']
            else:
                max_month = "Tidak ada data"
                max_count = 0
            
            print(f"📊 Auto stats: {total_reports} reports, year detected: {data_year}")
            
            return {
                'months_data': months_data,
                'total_reports': total_reports,
                'avg_per_month': round(avg_per_month, 1),
                'max_month': max_month,
                'max_count': max_count,
                'current_year_month': current_date.strftime('%Y-%m')
            }
            
        except Exception as e:
            print(f"❌ Error in auto stats: {e}")
            return self._get_yearly_stats_from_sqlite()
    
    def _extract_month_from_timestamp(self, timestamp_str):
        """Extract month from timestamp automatically"""
        try:
            # Format: "2025-12-20" → "2025-12"
            if '-' in timestamp_str:
                parts = timestamp_str.split('-')
                if len(parts) >= 2:
                    return f"{parts[0]}-{parts[1]}"
            
            # Format: "20/12/2025" → "2025-12"
            elif '/' in timestamp_str:
                parts = timestamp_str.split('/')
                if len(parts) >= 3:
                    return f"{parts[2]}-{parts[1]}"
            
            # Format: "Dec 20, 2025" → "2025-12"
            month_map = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            
            for month_name, month_num in month_map.items():
                if month_name in timestamp_str:
                    # Cari tahun
                    import re
                    year_match = re.search(r'\b(20\d{2})\b', timestamp_str)
                    year = year_match.group(1) if year_match else datetime.now().year
                    return f"{year}-{month_num}"
            
            return None
            
        except:
            return None
    
    def _detect_year_from_data(self, all_records):
        """Detect year from Google Sheets data automatically"""
        try:
            year_counts = {}
            
            for record in all_records:
                timestamp = record.get('Timestamp', '')
                if timestamp:
                    # Cari tahun 20xx
                    import re
                    year_match = re.search(r'\b(20\d{2})\b', str(timestamp))
                    if year_match:
                        year = year_match.group(1)
                        year_counts[year] = year_counts.get(year, 0) + 1
            
            # Return tahun dengan data terbanyak
            if year_counts:
                return max(year_counts, key=year_counts.get)
            
            return None
            
        except:
            return None
    
    def _get_yearly_stats_from_sqlite(self):
        """Fallback: Get stats from SQLite"""
        try:
            import sqlite3
            from datetime import datetime, timedelta
            
            conn = sqlite3.connect('flood_system.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flood_reports'")
            if not cursor.fetchone():
                conn.close()
                return self._get_empty_yearly_stats()
            
            cursor.execute("SELECT COUNT(*) FROM flood_reports")
            total_reports = cursor.fetchone()[0]
            
            current_date = datetime.now()
            months_data = []
            
            reports_per_month = total_reports // 12 if total_reports > 0 else 0
            remainder = total_reports % 12
            
            for i in range(11, -1, -1):
                target_date = current_date - timedelta(days=30*i)
                year_month = target_date.strftime('%Y-%m')
                month_name = target_date.strftime('%b')
                
                report_count = reports_per_month
                if i < remainder:
                    report_count += 1
                
                is_current = (year_month == current_date.strftime('%Y-%m'))
                
                months_data.append({
                    'year_month': year_month,
                    'month_name': month_name,
                    'report_count': report_count,
                    'is_current': is_current
                })
            
            conn.close()
            
            return {
                'months_data': months_data,
                'total_reports': total_reports,
                'avg_per_month': round(total_reports / 12, 1) if total_reports > 0 else 0,
                'max_month': "Estimasi" if total_reports > 0 else "Tidak ada data",
                'max_count': reports_per_month + 1 if remainder > 0 else reports_per_month,
                'current_year_month': current_date.strftime('%Y-%m')
            }
            
        except Exception as e:
            print(f"❌ SQLite stats error: {e}")
            return self._get_empty_yearly_stats()
    
    def _get_empty_yearly_stats(self):
        """Return empty yearly stats when error occurs"""
        return {
            'months_data': [],
            'total_reports': 0,
            'avg_per_month': 0,
            'max_month': "Tidak ada data",
            'max_count': 0,
            'current_year_month': datetime.now().strftime('%Y-%m') if hasattr(datetime, 'now') else ""
        }
    
    def get_client_ip(self):
        """Get client IP address"""
        try:
            if 'user_ip' not in st.session_state:
                import random
                st.session_state.user_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            
            ip = st.session_state.user_ip
            print(f"🖥️ Using IP: {ip}")
            return ip
            
        except Exception as e:
            print(f"⚠️ Error getting IP: {e}")
            return "unknown_user"
