from models.FloodReportModel import FloodReportModel
from models.GoogleSheetsModel import GoogleSheetsModel
from models.GoogleDriveModel import GoogleDriveModel
import os
import uuid
from datetime import datetime
import streamlit as st
import traceback

class FloodReportController:
    def __init__(self):
        print("🔄 Initializing FloodReportController...")
        
        try:
            self.flood_model = FloodReportModel()
            print("✅ Flood model initialized")
        except Exception as e:
            print(f"❌ Error initializing flood model: {e}")
            self.flood_model = None
        
        try:
            self.sheets_model = GoogleSheetsModel()
            if self.sheets_model and hasattr(self.sheets_model, 'client') and self.sheets_model.client:
                print("✅ Google Sheets connected")
            else:
                print("⚠️ Google Sheets offline")
                self.sheets_model = None
        except Exception as e:
            print(f"⚠️ Google Sheets init error: {e}")
            self.sheets_model = None
        
        try:
            self.drive_model = GoogleDriveModel()
            if self.drive_model and self.drive_model.service:
                print("✅ Google Drive connected")
            else:
                print("⚠️ Google Drive offline")
                self.drive_model = None
        except Exception as e:
            print(f"⚠️ Google Drive init error: {e}")
            self.drive_model = None
        
        print("✅ FloodReportController initialized")
    
    # ============ FORM SUBMISSION ============
    def submit_report(self, address, flood_height, reporter_name, reporter_phone=None, photo_file=None):
        """Submit new flood report"""
        try:
            print(f"📝 Submitting report: {address}")
            
            # Get client IP
            client_ip = self.get_client_ip()
            print(f"🌐 Client IP: {client_ip}")
            
            # Check daily limit
            if not self.check_daily_limit(client_ip):
                return False, "❌ Anda telah mencapai batas maksimal 10 laporan per hari."
            
            # Handle photo
            photo_info = None
            if photo_file is not None:
                photo_info = self._handle_photo_upload(photo_file)
                if photo_info is False:
                    return False, "❌ Error uploading photo"
            
            # Try to save to Google Sheets
            if self.sheets_model:
                try:
                    sheets_data = {
                        'address': str(address),
                        'flood_height': str(flood_height),
                        'reporter_name': str(reporter_name),
                        'reporter_phone': str(reporter_phone) if reporter_phone else '',
                        'ip_address': str(client_ip),
                        'photo_url': photo_info['view_url'] if photo_info else ''
                    }
                    
                    if self.sheets_model.save_flood_report(sheets_data):
                        print("✅ Saved to Google Sheets")
                        return True, "✅ Laporan berhasil dikirim ke Google Sheets!"
                    else:
                        print("⚠️ Failed to save to Google Sheets")
                except Exception as e:
                    print(f"⚠️ Google Sheets error: {e}")
            
            # Try SQLite as backup
            if self.flood_model:
                try:
                    photo_url = photo_info['direct_url'] if photo_info else None
                    report_id = self.flood_model.create_report(
                        alamat=address,
                        tinggi_banjir=flood_height,
                        nama_pelapor=reporter_name,
                        no_hp=reporter_phone,
                        photo_url=photo_url,
                        ip_address=client_ip
                    )
                    
                    if report_id:
                        print(f"✅ Saved to SQLite (ID: {report_id})")
                        return True, "✅ Laporan berhasil disimpan di database lokal!"
                    else:
                        print("⚠️ Failed to save to SQLite")
                except Exception as e:
                    print(f"⚠️ SQLite error: {e}")
            
            return False, "❌ Gagal menyimpan laporan"
                
        except Exception as e:
            print(f"❌ Error in submit_report: {e}")
            return False, f"❌ Error sistem: {str(e)}"
    
    def _handle_photo_upload(self, photo_file):
        """Handle photo upload"""
        try:
            file_extension = photo_file.name.split('.')[-1].lower()
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            
            if file_extension not in valid_extensions:
                print(f"❌ Invalid file extension: {file_extension}")
                return False
            
            file_bytes = photo_file.getbuffer().tobytes()
            filename = f"{uuid.uuid4()}.{file_extension}"
            
            if self.drive_model:
                upload_result = self.drive_model.upload_photo(file_bytes, filename)
                if upload_result:
                    print(f"✅ Photo uploaded to Google Drive")
                    return upload_result
            
            return None
                
        except Exception as e:
            print(f"❌ Error in photo upload: {e}")
            return None
    
    # ============ REPORT METHODS (WAJIB ADA) ============
    
    def get_today_reports(self):
        """Get today's flood reports"""
        try:
            if self.flood_model:
                return self.flood_model.get_today_reports()
            return []
        except Exception as e:
            print(f"⚠️ Error getting today reports: {e}")
            return []
    
    def get_month_reports(self):
        """Get this month's flood reports"""
        try:
            if self.flood_model:
                return self.flood_model.get_month_reports()
            return []
        except Exception as e:
            print(f"⚠️ Error getting month reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all flood reports"""
        try:
            if self.flood_model:
                return self.flood_model.get_all_reports()
            return []
        except Exception as e:
            print(f"⚠️ Error getting all reports: {e}")
            return []
    
    def get_monthly_statistics(self):
        """Get monthly statistics for reports"""
        try:
            if self.flood_model:
                return self.flood_model.get_monthly_statistics()
            return {'total_reports': 0, 'month': ''}
        except Exception as e:
            print(f"⚠️ Error getting statistics: {e}")
            return {'total_reports': 0, 'month': ''}
    
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
    
    def check_daily_limit(self, ip_address):
        """Check daily limit"""
        try:
            if self.flood_model:
                today_count = self.flood_model.get_today_reports_count_by_ip(ip_address)
                return today_count < 10
            return True
        except Exception as e:
            print(f"⚠️ Error checking daily limit: {e}")
            return True
    
    def is_google_sheets_available(self):
        """Check if Google Sheets is available"""
        return (self.sheets_model is not None and 
                hasattr(self.sheets_model, 'client') and 
                self.sheets_model.client is not None)
    
    def is_google_drive_available(self):
        """Check if Google Drive is available"""
        return (self.drive_model is not None and 
                self.drive_model.service is not None)
