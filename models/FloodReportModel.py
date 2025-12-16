import sqlite3
from datetime import datetime
import os
import traceback

class FloodReportModel:
    def __init__(self, db_path='flood_system.db'):
        self.db_path = db_path
        print(f"📂 Database path: {os.path.abspath(db_path)}")
        self.init_database()
    
    def init_database(self):
        """Initialize database with photo_base64 column"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Buat tabel dengan kolom photo_base64
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flood_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        address TEXT NOT NULL,
                        flood_height TEXT NOT NULL,
                        reporter_name TEXT NOT NULL,
                        reporter_phone TEXT,
                        photo_path TEXT,
                        photo_base64 TEXT,  -- NEW: Store Base64 string
                        ip_address TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                print("✅ Database table flood_reports ready (with photo_base64)")
                
        except Exception as e:
            print(f"❌ Error in init_database: {e}")
            traceback.print_exc()
    
    def create_report(self, address, flood_height, reporter_name, 
                      reporter_phone=None, photo_path=None, photo_base64=None, ip_address=None):
        """Create new flood report with Base64 photo"""
        try:
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f" Creating report with Base64 photo: {photo_base64[:50] if photo_base64 else 'No photo'}...")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO flood_reports 
                    (timestamp, address, flood_height, reporter_name, reporter_phone, 
                     photo_path, photo_base64, ip_address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    str(address) if address else "",
                    str(flood_height) if flood_height else "",
                    str(reporter_name) if reporter_name else "",
                    str(reporter_phone) if reporter_phone else None,
                    str(photo_path) if photo_path else None,
                    str(photo_base64) if photo_base64 else None,  # Store Base64
                    str(ip_address) if ip_address else "unknown"
                ))
                
                conn.commit()
                last_id = cursor.lastrowid
                print(f"✅ Report created with ID: {last_id}")
                
                return last_id
                
        except Exception as e:
            print(f"❌ Error creating report: {e}")
            traceback.print_exc()
            return None
    
    def get_today_reports(self):
        """Get today's reports with Base64 photos"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id,
                        timestamp,
                        address,
                        flood_height,
                        reporter_name,
                        reporter_phone,
                        photo_path,
                        photo_base64,  -- Include Base64
                        ip_address
                    FROM flood_reports 
                    WHERE DATE(timestamp) = ?
                    ORDER BY timestamp DESC
                ''', (today,))
                
                rows = cursor.fetchall()
                reports = []
                
                for row in rows:
                    # Parse timestamp
                    try:
                        timestamp = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                        report_date = timestamp.strftime('%Y-%m-%d')
                        report_time = timestamp.strftime('%H:%M:%S')
                    except:
                        report_date = row[1][:10] if row[1] else "N/A"
                        report_time = row[1][11:19] if row[1] and len(row[1]) > 11 else "N/A"
                    
                    reports.append({
                        'id': row[0],
                        'address': row[2],
                        'flood_height': row[3],
                        'reporter_name': row[4],
                        'reporter_phone': row[5],
                        'photo_path': row[6],
                        'photo_base64': row[7],  # Base64 string
                        'ip_address': row[8],
                        'report_date': report_date,
                        'report_time': report_time,
                        'timestamp': row[1]
                    })
                
                print(f" Today's reports: {len(reports)} (with Base64 photos)")
                return reports
                
        except Exception as e:
            print(f"❌ Error getting today's reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get this month's reports with Base64 photos"""
        try:
            current_month = datetime.now().strftime("%Y-%m")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        id,
                        timestamp,
                        address,
                        flood_height,
                        reporter_name,
                        reporter_phone,
                        photo_path,
                        photo_base64,  -- Include Base64
                        ip_address
                    FROM flood_reports 
                    WHERE strftime('%Y-%m', timestamp) = ?
                    ORDER BY timestamp DESC
                ''', (current_month,))
                
                rows = cursor.fetchall()
                reports = []
                
                for row in rows:
                    # Parse timestamp
                    try:
                        timestamp = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                        report_date = timestamp.strftime('%Y-%m-%d')
                        report_time = timestamp.strftime('%H:%M:%S')
                    except:
                        report_date = row[1][:10] if row[1] else "N/A"
                        report_time = row[1][11:19] if row[1] and len(row[1]) > 11 else "N/A"
                    
                    reports.append({
                        'id': row[0],
                        'address': row[2],
                        'flood_height': row[3],
                        'reporter_name': row[4],
                        'reporter_phone': row[5],
                        'photo_path': row[6],
                        'photo_base64': row[7],  # Base64 string
                        'ip_address': row[8],
                        'report_date': report_date,
                        'report_time': report_time,
                        'timestamp': row[1]
                    })
                
                print(f" Month's reports: {len(reports)} (with Base64 photos)")
                return reports
                
        except Exception as e:
            print(f"❌ Error getting month's reports: {e}")
            return []
    
    # ... [other methods remain similar, just include photo_base64 in queries]
