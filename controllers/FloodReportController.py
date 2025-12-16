from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
import os
import uuid
from datetime import datetime, timezone, timedelta
import streamlit as st

class FloodReportController:
    def __init__(self):
        # Initialize database model
        self.flood_model = FloodReportModel()
        self.sheets_model = None
        
        # Initialize Google Sheets hanya untuk TAB 1
        try:
            self.sheets_model = GoogleSheetsModel()
            if self.sheets_model.client:
                print("✅ Google Sheets connected for flood reports")
            else:
                print("⚠️ Google Sheets offline - using SQLite only")
                self.sheets_model = None
        except Exception as e:
            print(f"⚠️ Google Sheets init error: {e}")
            self.sheets_model = None
        
        # Setup upload folder
        self.upload_folder = "uploads"
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
    
    def get_wib_time(self):
        """Get current time in WIB (UTC+7)"""
        utc_now = datetime.now(timezone.utc)
        wib_time = utc_now + timedelta(hours=7)
        return wib_time

    def check_daily_limit(self, ip_address):
        """Check if daily limit (10 reports per IP) has been reached"""
        try:
            today_count = self.flood_model.get_today_reports_count_by_ip(ip_address)
            return today_count < 10
        except Exception as e:
            print(f"⚠️ Error in check_daily_limit: {e}")
            return True

    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report - ke SQLite dan Google Sheets (TAB 1 saja)"""
        photo_path = None
        photo_url = None
        
        try:
            # Get client IP
            client_ip = self.get_client_ip()
            
            # Check daily limit
            if not self.check_daily_limit(client_ip):
                return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari."
            
            # Handle photo upload
            if photo_file is not None:
                try:
                    file_extension = photo_file.name.split('.')[-1].lower()
                    filename = f"{uuid.uuid4()}.{file_extension}"
                    photo_path = os.path.join(self.upload_folder, filename)
                    
                    with open(photo_path, "wb") as f:
                        f.write(photo_file.getbuffer())
                    
                    photo_url = f"uploads/{filename}"
                    print(f"✅ Photo saved: {photo_url}")
                    
                except Exception as e:
                    print(f"❌ Error saving photo: {e}")
            
            # ========== SIMPAN KE SQLITE DATABASE ==========
            print("📊 Saving to SQLite database...")
            report_id = self.flood_model.create_report(
                address=address,
                flood_height=flood_height,
                reporter_name=reporter_name,
                reporter_phone=reporter_phone,
                photo_path=photo_path,
                ip_address=client_ip
            )
            
            if not report_id:
                if photo_path and os.path.exists(photo_path):
                    os.remove(photo_path)
                return False, "❌ Gagal menyimpan laporan ke database lokal"
            
            print(f"✅ Saved to SQLite (ID: {report_id})")
            
            # ========== SIMPAN KE GOOGLE SHEETS TAB 1 ==========
            if self.sheets_model and self.sheets_model.client:
                try:
                    print("☁️ Saving to Google Sheets...")
                    sheets_data = {
                        'address': address,
                        'flood_height': flood_height,
                        'reporter_name': reporter_name,
                        'reporter_phone': reporter_phone or '',
                        'ip_address': client_ip,
                        'photo_url': photo_url or ''
                    }
                    
                    success = self.sheets_model.save_flood_report(sheets_data)
                    if success:
                        print("✅ Report saved to Google Sheets")
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                        
                except Exception as e:
                    print(f"⚠️ Error saving to Google Sheets: {e}")
            else:
                print("ℹ️ Google Sheets not available, only saved to SQLite")
            
            return True, "✅ Laporan berhasil dikirim!"
                
        except Exception as e:
            print(f"❌ Error in submit_report: {e}")
            if photo_path and os.path.exists(photo_path):
                os.remove(photo_path)
            return False, f"❌ Error: {str(e)}"
    
    # ============ FUNGSI UNTUK VIEWS ============
    
    def get_today_reports(self):
        """Get today's flood reports"""
        return self.flood_model.get_today_reports()

    def get_month_reports(self):
        """Get this month's flood reports"""
        return self.flood_model.get_month_reports()

    def get_all_reports(self):
        """Get all flood reports"""
        return self.flood_model.get_all_reports()
    
    def get_monthly_statistics(self):
        """Get monthly statistics for reports"""
        return self.flood_model.get_monthly_statistics()
    
    def get_client_ip(self):
        """Get client IP address"""
        try:
            if 'user_ip' not in st.session_state:
                import random
                # Generate IP address untuk testing
                st.session_state.user_ip = f"192.168.1.{random.randint(1, 255)}"
            return st.session_state.user_ip
        except:
            return "user_local_test"
    
    def get_current_wib_time(self):
        """Get current WIB time for display"""
        wib_time = self.get_wib_time()
        return wib_time.strftime("%Y-%m-%d %H:%M:%S WIB")
