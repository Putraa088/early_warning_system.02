import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import os
import pytz
import time
import socket
import json

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.tz_wib = pytz.timezone('Asia/Jakarta')
        self.setup_connection()
    
    def setup_connection(self):
        """Setup Google Sheets connection"""
        try:
            print("🔄 Setting up Google Sheets connection...")
            
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Coba dari Streamlit Secrets
            if 'GOOGLE_SHEETS' in st.secrets:
                print("🔑 Using Streamlit Secrets")
                gs_secrets = st.secrets['GOOGLE_SHEETS']
                
                credentials_data = {
                    "type": "service_account",
                    "project_id": gs_secrets.get('project_id', ''),
                    "private_key_id": gs_secrets.get('private_key_id', ''),
                    "private_key": gs_secrets.get('private_key', '').replace('\\n', '\n'),
                    "client_email": gs_secrets.get('client_email', ''),
                    "client_id": gs_secrets.get('client_id', ''),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": gs_secrets.get('client_x509_cert_url', '')
                }
                
            # Fallback ke credentials.json
            elif os.path.exists('credentials.json'):
                print("🔑 Using credentials.json")
                with open('credentials.json', 'r') as f:
                    credentials_data = json.load(f)
            
            else:
                print("❌ No Google Sheets credentials found")
                self.client = None
                return
            
            # Authorize
            creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_data, scope)
            self.client = gspread.authorize(creds)
            print("✅ Google Sheets API authorized")
            
            # Open spreadsheet
            spreadsheet_id = st.secrets.get('GOOGLE_SHEETS', {}).get('SPREADSHEET_ID', 
                          '1wdys3GzfDfl0ohCQjUHRyJVbKQcM0VSIMgCryHB0-mc')
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            print(f"✅ Spreadsheet opened: {self.spreadsheet.title}")
            
            # Get worksheet
            self.worksheet = self.spreadsheet.worksheet('flood_reports')
            print(f"✅ Worksheet ready: {self.worksheet.title}")
            print(f"📊 Current rows: {self.worksheet.row_count}")
            
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            self.client = None
    
    def save_flood_report(self, report_data):
        """Save report to Google Sheets"""
        try:
            if not self.worksheet:
                print("❌ Worksheet not available")
                return False
            
            # Waktu WIB
            current_time_wib = datetime.now(self.tz_wib)
            timestamp_wib = current_time_wib.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"📊 Saving to Google Sheets...")
            
            # Row data
            row = [
                timestamp_wib,                      # A: Timestamp
                str(report_data.get('address', '')),     # B: Alamat
                str(report_data.get('flood_height', '')), # C: Tinggi Banjir
                str(report_data.get('reporter_name', '')), # D: Nama Pelapor
                str(report_data.get('reporter_phone', '')), # E: No HP
                str(report_data.get('ip_address', '')),   # F: IP Address
                str(report_data.get('photo_url', '')),    # G: Photo URL
                'pending'                           # H: Status
            ]
            
            # Append row
            self.worksheet.append_row(row)
            print("✅ Saved to Google Sheets!")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to Google Sheets: {e}")
            return False
