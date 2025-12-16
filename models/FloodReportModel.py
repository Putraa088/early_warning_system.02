import sqlite3
from datetime import datetime
import os
import traceback

class FloodReportModel:
    def __init__(self, db_path='flood_system.db'):
        self.db_path = db_path
        print(f"📂 Database path: {os.path.abspath(db_path)}")
        self._force_init_database()
    
    def _force_init_database(self):
        """Force initialize database - HAPUS DAN BUAT ULANG"""
        try:
            # Hapus database lama jika ada
            if os.path.exists(self.db_path):
                print(f"🗑️ Removing old database: {self.db_path}")
                os.remove(self.db_path)
            
            # Buat koneksi baru
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # BUAT TABEL SANGAT SEDERHANA
            cursor.execute('''
                CREATE TABLE flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    address TEXT,
                    flood_height TEXT,
                    reporter_name TEXT,
                    reporter_phone TEXT,
                    photo_path TEXT,
                    ip_address TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Database created from scratch")
            
            # Test insert langsung
            self._test_database()
            
        except Exception as e:
            print(f"❌ CRITICAL: Cannot create database: {e}")
            traceback.print_exc()
    
    def _test_database(self):
        """Test database connection and insert"""
        try:
            print("🧪 Testing database...")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test insert
            test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO flood_reports 
                (timestamp, address, flood_height, reporter_name, ip_address)
                VALUES (?, ?, ?, ?, ?)
            ''', (test_time, "TEST ADDRESS", "TEST HEIGHT", "TEST USER", "127.0.0.1"))
            
            conn.commit()
            
            # Test select
            cursor.execute('SELECT COUNT(*) FROM flood_reports')
            count = cursor.fetchone()[0]
            print(f"✅ Test insert successful! Total records: {count}")
            
            # Show all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✅ Tables in database: {tables}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            traceback.print_exc()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"❌ Cannot connect to database: {e}")
            return None
    
    def create_report(self, address, flood_height, reporter_name, 
                      reporter_phone=None, photo_path=None, ip_address=None):
        """Create new flood report - EXTREME SIMPLIFICATION"""
        try:
            if not self.get_connection():
                print("❌ No database connection")
                return None
            
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"📝 CREATE REPORT CALLED:")
            print(f"   Address: '{address}'")
            print(f"   Height: '{flood_height}'")
            print(f"   Name: '{reporter_name}'")
            print(f"   Phone: '{reporter_phone}'")
            print(f"   Photo: '{photo_path}'")
            print(f"   IP: '{ip_address}'")
            print(f"   Time: '{timestamp}'")
            
            conn = self.get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor()
            
            # INSERT dengan try-catch detail
            try:
                cursor.execute('''
                    INSERT INTO flood_reports 
                    (timestamp, address, flood_height, reporter_name, reporter_phone, photo_path, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(timestamp),
                    str(address) if address else "",
                    str(flood_height) if flood_height else "",
                    str(reporter_name) if reporter_name else "",
                    str(reporter_phone) if reporter_phone else None,
                    str(photo_path) if photo_path else None,
                    str(ip_address) if ip_address else "unknown"
                ))
                
                conn.commit()
                last_id = cursor.lastrowid
                print(f"✅ INSERT successful! ID: {last_id}")
                
                # VERIFY with direct query
                cursor.execute('SELECT * FROM flood_reports WHERE id = ?', (last_id,))
                row = cursor.fetchone()
                
                if row:
                    print(f"✅ VERIFICATION PASSED:")
                    print(f"   ID: {row['id']}")
                    print(f"   Address: {row['address']}")
                    print(f"   Timestamp: {row['timestamp']}")
                else:
                    print("❌ VERIFICATION FAILED: Row not found!")
                
                conn.close()
                return last_id
                
            except sqlite3.Error as e:
                print(f"❌ SQLite error during INSERT: {e}")
                print(f"❌ SQLite error details: {e.__class__.__name__}")
                conn.rollback()
                conn.close()
                return None
                
        except Exception as e:
            print(f"❌ UNEXPECTED error in create_report: {e}")
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
            
            print(f"📊 Count for IP {ip_address} today: {count}")
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
                # Parse timestamp untuk date/time
                try:
                    dt = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                    report_date = dt.strftime('%Y-%m-%d')
                    report_time = dt.strftime('%H:%M:%S')
                except:
                    report_date = "N/A"
                    report_time = "N/A"
                
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
