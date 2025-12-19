import sqlite3
import os
from datetime import datetime
import pytz

class FloodReportModel:
    def __init__(self, db_path=None):
        if not db_path:
            if 'STREAMLIT_CLOUD' in os.environ:
                db_path = '/mount/src/early_warning_system/flood_system.db'
            else:
                db_path = 'flood_system.db'
        
        self.db_path = db_path
        self.tz_wib = pytz.timezone('Asia/Jakarta')
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Timestamp TEXT,
                    Alamat TEXT,
                    "Tinggi Banjir" TEXT,
                    "Nama Pelapor" TEXT,
                    "No HP" TEXT,
                    "IP Address" TEXT,
                    "Photo URL" TEXT,
                    Status TEXT DEFAULT 'pending',
                    report_date DATE,
                    report_time TIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print(f"✅ Database initialized: {self.db_path}")
        except Exception as e:
            print(f"❌ Database init error: {e}")
    
    def create_report(self, alamat, tinggi_banjir, nama_pelapor, no_hp=None, photo_url=None, ip_address=None):
        """Create new report"""
        try:
            timestamp = datetime.now(self.tz_wib).strftime("%Y-%m-%d %H:%M:%S")
            report_date = datetime.now(self.tz_wib).strftime("%Y-%m-%d")
            report_time = datetime.now(self.tz_wib).strftime("%H:%M:%S")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO flood_reports 
                (Timestamp, Alamat, "Tinggi Banjir", "Nama Pelapor", 
                 "No HP", "IP Address", "Photo URL", Status,
                 report_date, report_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, alamat, tinggi_banjir, nama_pelapor, 
                  no_hp, ip_address, photo_url, 'pending',
                  report_date, report_time))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Report created: ID {report_id}")
            return report_id
        except Exception as e:
            print(f"❌ Create report error: {e}")
            return None
    
    def get_today_reports(self):
        """Get today's reports"""
        try:
            today = datetime.now(self.tz_wib).strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE report_date = ? 
                ORDER BY Timestamp DESC
            ''', (today,))
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = [dict(row) for row in rows]
            print(f"📊 Today's reports: {len(reports)}")
            return reports
        except Exception as e:
            print(f"❌ Get today reports error: {e}")
            return []
    
    def get_month_reports(self):
        """Get month's reports"""
        try:
            current_month = datetime.now(self.tz_wib).strftime("%Y-%m")
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ? 
                ORDER BY Timestamp DESC
            ''', (current_month,))
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = [dict(row) for row in rows]
            print(f"📊 Month's reports: {len(reports)}")
            return reports
        except Exception as e:
            print(f"❌ Get month reports error: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM flood_reports ORDER BY Timestamp DESC')
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except:
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics"""
        try:
            current_month = datetime.now(self.tz_wib).strftime("%Y-%m")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
            ''', (current_month,))
            
            total = cursor.fetchone()[0]
            conn.close()
            
            return {'total_reports': total, 'month': current_month}
        except:
            return {'total_reports': 0, 'month': ''}
    
    def get_today_reports_count_by_ip(self, ip_address):
        """Count today's reports by IP"""
        try:
            today = datetime.now(self.tz_wib).strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE "IP Address" = ? AND report_date = ?
            ''', (ip_address, today))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count
        except:
            return 0
