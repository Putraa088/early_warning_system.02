import sqlite3
import os
from datetime import datetime

class FloodReportModel:
    _initialized = False
    
    def __init__(self):
        self.db_path = 'flood_system.db'
        if not FloodReportModel._initialized:
            self.init_database()
            FloodReportModel._initialized = True

    def init_database(self):
        """Initialize database and tables for flood reports"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create flood_reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flood_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    flood_height TEXT NOT NULL,
                    reporter_name TEXT NOT NULL,
                    reporter_phone TEXT,
                    photo_path TEXT,
                    ip_address TEXT,
                    report_date DATE DEFAULT CURRENT_DATE,
                    report_time TIME DEFAULT CURRENT_TIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            
            # Create index untuk sorting yang optimal
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_report_datetime 
                ON flood_reports(report_date DESC, report_time DESC, created_at DESC)
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Database flood_reports initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def create_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_path=None, ip_address=None):
        """Create new flood report"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Gunakan tanggal dan waktu saat ini
            today_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            
            cursor.execute('''
                INSERT INTO flood_reports 
                (address, flood_height, reporter_name, reporter_phone, photo_path, ip_address, report_date, report_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (address, flood_height, reporter_name, reporter_phone, photo_path, ip_address, today_date, current_time))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Report #{report_id} created on {today_date} at {current_time}")
            return report_id
            
        except Exception as e:
            print(f"❌ Error creating flood report: {e}")
            return None

    def get_today_reports_count_by_ip(self, ip_address):
        """Get count of today's reports by IP address"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            today_date = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE report_date = ? AND ip_address = ?
            ''', (today_date, ip_address))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            print(f"📊 Count for IP '{ip_address}' today: {count}")
            return count
            
        except Exception as e:
            print(f"❌ Error in get_today_reports_count_by_ip: {e}")
            return 0

    def get_today_reports(self):
        """Get all flood reports for today - TERBARU DI ATAS"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            today_date = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE report_date = ?
                ORDER BY 
                    report_time DESC,
                    created_at DESC,
                    id DESC
            ''', (today_date,))
            
            reports = cursor.fetchall()
            conn.close()
            
            columns = ['id', 'address', 'flood_height', 'reporter_name', 'reporter_phone', 
                    'photo_path', 'ip_address', 'report_date', 'report_time', 'created_at', 'status']
            
            result = [dict(zip(columns, report)) for report in reports]
            print(f"📄 Today's reports: {len(result)} found (newest first)")
            return result
            
        except Exception as e:
            print(f"❌ Error getting today reports: {e}")
            return []

    def get_month_reports(self):
        """Get all flood reports for current month - TERBARU DI ATAS"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            current_month = datetime.now().strftime('%Y-%m')
            
            # ORDER BY: tanggal DESC, waktu DESC, created_at DESC, id DESC
            cursor.execute('''
                SELECT * FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
                ORDER BY 
                    report_date DESC,
                    report_time DESC,
                    created_at DESC,
                    id DESC
            ''', (current_month,))
            
            reports = cursor.fetchall()
            conn.close()
            
            columns = ['id', 'address', 'flood_height', 'reporter_name', 'reporter_phone', 
                    'photo_path', 'ip_address', 'report_date', 'report_time', 'created_at', 'status']
            
            result = [dict(zip(columns, report)) for report in reports]
            
            # Debug: tampilkan urutan
            if result:
                print(f"📅 Month reports ({current_month}): {len(result)} found")
                print(f"   First (newest): ID:{result[0]['id']} | {result[0]['report_date']} {result[0]['report_time']}")
                if len(result) > 1:
                    print(f"   Last (oldest): ID:{result[-1]['id']} | {result[-1]['report_date']} {result[-1]['report_time']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error getting month reports: {e}")
            return []

    def get_all_reports(self):
        """Get all flood reports - TERBARU DI ATAS"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM flood_reports 
                ORDER BY 
                    report_date DESC,
                    report_time DESC,
                    created_at DESC,
                    id DESC
            ''')
            
            reports = cursor.fetchall()
            conn.close()
            
            columns = ['id', 'address', 'flood_height', 'reporter_name', 'reporter_phone', 
                    'photo_path', 'ip_address', 'report_date', 'report_time', 'created_at', 'status']
            return [dict(zip(columns, report)) for report in reports]
            
        except Exception as e:
            print(f"❌ Error getting all reports: {e}")
            return []

    def get_monthly_statistics(self):
        """Get monthly statistics for reports"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            current_month = datetime.now().strftime('%Y-%m')
            
            # Total reports this month
            cursor.execute('''
                SELECT COUNT(*) FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
            ''', (current_month,))
            total_reports = cursor.fetchone()[0]
            
            # Average reports per day
            cursor.execute('''
                SELECT COUNT(DISTINCT report_date) FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
            ''', (current_month,))
            days_with_reports = cursor.fetchone()[0]
            avg_per_day = total_reports / days_with_reports if days_with_reports > 0 else 0
            
            # Most common flood height
            cursor.execute('''
                SELECT flood_height, COUNT(*) as count 
                FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
                GROUP BY flood_height 
                ORDER BY count DESC 
                LIMIT 1
            ''', (current_month,))
            most_common_height = cursor.fetchone()
            
            # Most affected area
            cursor.execute('''
                SELECT address, COUNT(*) as count 
                FROM flood_reports 
                WHERE strftime('%Y-%m', report_date) = ?
                GROUP BY address 
                ORDER BY count DESC 
                LIMIT 1
            ''', (current_month,))
            most_affected_area = cursor.fetchone()
            
            conn.close()
            
            return {
                'total_reports': total_reports,
                'avg_per_day': round(avg_per_day, 1),
                'most_common_height': most_common_height[0] if most_common_height else 'Tidak ada data',
                'most_common_height_count': most_common_height[1] if most_common_height else 0,
                'most_affected_area': most_affected_area[0] if most_affected_area else 'Tidak ada data',
                'most_affected_area_count': most_affected_area[1] if most_affected_area else 0
            }
            
        except Exception as e:
            print(f"❌ Error getting monthly statistics: {e}")
            return {
                'total_reports': 0,
                'avg_per_day': 0,
                'most_common_height': 'Error',
                'most_common_height_count': 0,
                'most_affected_area': 'Error',
                'most_affected_area_count': 0
            }
