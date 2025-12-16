import sqlite3
from datetime import datetime
import os
import traceback

class FloodReportModel:
    def __init__(self, db_path='flood_system.db'):
        self.db_path = db_path
        print(f"📂 Database path: {os.path.abspath(db_path)}")
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"❌ Cannot connect to database: {e}")
            return None
    
    def init_database(self):
        """Initialize database dengan struktur yang benar"""
        try:
            # Hapus database lama jika ada masalah
            if os.path.exists(self.db_path):
                print(f"ℹ️ Database exists: {os.path.getsize(self.db_path)} bytes")
            
            conn = self.get_connection()
            if not conn:
                # Buat database baru
                conn = sqlite3.connect(self.db_path)
            
            cursor = conn.cursor()
            
            # Buat tabel jika belum ada
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    address TEXT NOT NULL,
                    flood_height TEXT NOT NULL,
                    reporter_name TEXT NOT NULL,
                    reporter_phone TEXT,
                    photo_path TEXT,
                    ip_address TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # Cek struktur tabel
            cursor.execute("PRAGMA table_info(flood_reports)")
            columns = cursor.fetchall()
            print(f"✅ Table 'flood_reports' ready with {len(columns)} columns")
            
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error in init_database: {e}")
            traceback.print_exc()
            return False
    
    def create_report(self, address, flood_height, reporter_name, 
                      reporter_phone=None, photo_path=None, ip_address=None):
        """Create new flood report"""
        try:
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"📝 Creating report:")
            print(f"  Address: {address}")
            print(f"  Height: {flood_height}")
            print(f"  Name: {reporter_name}")
            print(f"  Phone: {reporter_phone}")
            print(f"  Photo: {photo_path}")
            print(f"  IP: {ip_address}")
            print(f"  Time: {timestamp}")
            
            conn = self.get_connection()
            if not conn:
                print("❌ No database connection")
                return None
            
            cursor = conn.cursor()
            
            # INSERT data
            cursor.execute('''
                INSERT INTO flood_reports 
                (timestamp, address, flood_height, reporter_name, reporter_phone, 
                 photo_path, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                str(address) if address else "",
                str(flood_height) if flood_height else "",
                str(reporter_name) if reporter_name else "",
                str(reporter_phone) if reporter_phone else None,
                str(photo_path) if photo_path else None,
                str(ip_address) if ip_address else "unknown"
            ))
            
            conn.commit()
            last_id = cursor.lastrowid
            print(f"✅ Report created with ID: {last_id}")
            
            # Verifikasi
            cursor.execute('SELECT COUNT(*) FROM flood_reports')
            count = cursor.fetchone()[0]
            print(f"✅ Total reports in database: {count}")
            
            conn.close()
            return last_id
            
        except Exception as e:
            print(f"❌ Error creating report: {e}")
            traceback.print_exc()
            return None
    
    def get_today_reports_count_by_ip(self, ip_address):
        """Count today's reports by IP address"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            conn = self.get_connection()
            if not conn:
                return 0
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE ip_address = ? AND DATE(timestamp) = ?
            ''', (ip_address, today))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            print(f"📊 Today's reports for IP {ip_address}: {count}")
            return count
            
        except Exception as e:
            print(f"❌ Error counting reports: {e}")
            return 0
    
    def get_today_reports(self):
        """Get today's reports"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE DATE(timestamp) = ?
                ORDER BY timestamp DESC
            ''', (today,))
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = []
            for row in rows:
                # Parse timestamp untuk report_date dan report_time
                try:
                    timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                    report_date = timestamp.strftime('%Y-%m-%d')
                    report_time = timestamp.strftime('%H:%M:%S')
                except:
                    report_date = row['timestamp'][:10] if row['timestamp'] else "N/A"
                    report_time = row['timestamp'][11:19] if row['timestamp'] and len(row['timestamp']) > 11 else "N/A"
                
                reports.append({
                    'id': row['id'],
                    'address': row['address'],
                    'flood_height': row['flood_height'],
                    'reporter_name': row['reporter_name'],
                    'reporter_phone': row['reporter_phone'],
                    'photo_path': row['photo_path'],
                    'ip_address': row['ip_address'],
                    'report_date': report_date,
                    'report_time': report_time,
                    'timestamp': row['timestamp']
                })
            
            print(f"📊 Today's reports: {len(reports)}")
            return reports
            
        except Exception as e:
            print(f"❌ Error getting today's reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get this month's reports"""
        try:
            current_month = datetime.now().strftime("%Y-%m")
            
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE strftime('%Y-%m', timestamp) = ?
                ORDER BY timestamp DESC
            ''', (current_month,))
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = []
            for row in rows:
                # Parse timestamp untuk report_date dan report_time
                try:
                    timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                    report_date = timestamp.strftime('%Y-%m-%d')
                    report_time = timestamp.strftime('%H:%M:%S')
                except:
                    report_date = row['timestamp'][:10] if row['timestamp'] else "N/A"
                    report_time = row['timestamp'][11:19] if row['timestamp'] and len(row['timestamp']) > 11 else "N/A"
                
                reports.append({
                    'id': row['id'],
                    'address': row['address'],
                    'flood_height': row['flood_height'],
                    'reporter_name': row['reporter_name'],
                    'reporter_phone': row['reporter_phone'],
                    'photo_path': row['photo_path'],
                    'ip_address': row['ip_address'],
                    'report_date': report_date,
                    'report_time': report_time,
                    'timestamp': row['timestamp']
                })
            
            print(f"📊 Month's reports: {len(reports)}")
            return reports
            
        except Exception as e:
            print(f"❌ Error getting month's reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports"""
        try:
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM flood_reports ORDER BY timestamp DESC')
            
            rows = cursor.fetchall()
            conn.close()
            
            reports = []
            for row in rows:
                reports.append({
                    'id': row['id'],
                    'address': row['address'],
                    'flood_height': row['flood_height'],
                    'reporter_name': row['reporter_name'],
                    'reporter_phone': row['reporter_phone'],
                    'photo_path': row['photo_path'],
                    'ip_address': row['ip_address'],
                    'timestamp': row['timestamp']
                })
            
            return reports
            
        except Exception as e:
            print(f"❌ Error getting all reports: {e}")
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics"""
        try:
            current_month = datetime.now().strftime("%Y-%m")
            
            conn = self.get_connection()
            if not conn:
                return {'total_reports': 0, 'month': current_month}
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE strftime('%Y-%m', timestamp) = ?
            ''', (current_month,))
            
            total = cursor.fetchone()[0]
            conn.close()
            
            return {
                'total_reports': total,
                'month': current_month
            }
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {'total_reports': 0, 'month': ''}
