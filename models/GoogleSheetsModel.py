import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import os

class GoogleSheetsModel:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.client = None
        self.spreadsheet = None
        self.setup_connection()
    
def setup_connection(self):
    """Setup connection to Google Sheets dengan debug detail"""
    try:
        print("🔧 Setting up Google Sheets connection...")
        
        # Scope
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        # Check credentials source
        if 'GOOGLE_SHEETS' in st.secrets:
            print("✅ Using Streamlit Secrets")
            secrets = st.secrets["GOOGLE_SHEETS"]
            
            # Debug: Print available keys
            print(f"📋 Available keys in secrets: {list(secrets.keys())}")
            
            # Check required keys
            required_keys = ['project_id', 'private_key_id', 'private_key', 'client_email', 'SPREADSHEET_ID']
            missing_keys = [key for key in required_keys if key not in secrets]
            
            if missing_keys:
                print(f"❌ MISSING keys in secrets: {missing_keys}")
                return
            
            credentials_dict = {
                "type": "service_account",
                "project_id": secrets["project_id"],
                "private_key_id": secrets["private_key_id"],
                "private_key": secrets["private_key"].replace('\\n', '\n'),
                "client_email": secrets["client_email"],
                "client_id": secrets.get("client_id", ""),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": secrets.get("client_x509_cert_url", "")
            }
            
            print(f"📧 Service Account: {secrets['client_email']}")
            print(f"📄 Project ID: {secrets['project_id']}")
            print(f"🔑 Has SPREADSHEET_ID: {'SPREADSHEET_ID' in secrets}")
            
            creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        
        elif os.path.exists('credentials.json'):
            print("✅ Using local credentials.json")
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        else:
            print("❌ No credentials found")
            return
        
        # Authorize
        print("🔄 Authorizing with Google...")
        self.client = gspread.authorize(creds)
        print("✅ Authorization successful")
        
        # Get spreadsheet
        spreadsheet_id = st.secrets["GOOGLE_SHEETS"]["SPREADSHEET_ID"]
        print(f"📊 Opening spreadsheet ID: {spreadsheet_id}")
        
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)
        print(f"✅ Connected to: {self.spreadsheet.title}")
        print(f"📋 Available worksheets: {[ws.title for ws in self.spreadsheet.worksheets()]}")
        
    except Exception as e:
        print(f"❌ Google Sheets connection FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        self.client = None
        self.spreadsheet = None
    
    def get_worksheet(self, sheet_name):
        """Get worksheet by name"""
        if not self.spreadsheet:
            print(f"❌ Spreadsheet not initialized")
            return None
        
        try:
            return self.spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            print(f"❌ Worksheet '{sheet_name}' not found")
            return None
        except Exception as e:
            print(f"❌ Error getting worksheet: {e}")
            return None
    
    # ========== TAB 1: flood_reports ==========
    
    def save_flood_report(self, report_data):
        """Save flood report to Google Sheets (TAB 1)"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                return False
            
            # Prepare data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                timestamp,                           # Timestamp
                report_data.get('address', ''),      # Alamat
                report_data.get('flood_height', ''), # Tinggi Banjir
                report_data.get('reporter_name', ''), # Nama Pelapor
                report_data.get('reporter_phone', ''), # No HP
                report_data.get('ip_address', ''),   # IP Address
                report_data.get('photo_url', ''),    # Photo URL
                'pending'                           # Status
            ]
            
            # Append to sheet
            ws.append_row(row)
            print(f"✅ Report saved to Google Sheets at {timestamp}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving flood report: {e}")
            return False
    
    def get_recent_reports(self, limit=100):
        """Get recent flood reports from Google Sheets"""
        try:
            ws = self.get_worksheet("flood_reports")
            if not ws:
                return []
            
            # Get all data
            all_data = ws.get_all_values()
            if len(all_data) <= 1:  # Only header or empty
                return []
            
            # Convert to list of dictionaries
            headers = all_data[0]
            rows = all_data[1:]  # Skip header
            
            # Get latest reports (reverse order)
            recent_rows = rows[-limit:] if len(rows) > limit else rows
            recent_rows.reverse()  # Newest first
            
            reports = []
            for row in recent_rows:
                if len(row) >= len(headers):  # Ensure row has enough columns
                    report = {headers[i]: row[i] for i in range(len(headers))}
                    reports.append(report)
            
            return reports
            
        except Exception as e:
            print(f"❌ Error getting reports: {e}")
            return []
    
    # ========== TAB 2: predictions ==========
    
    def save_prediction(self, prediction_data):
        """Save prediction data to Google Sheets (TAB 2)"""
        try:
            ws = self.get_worksheet("predictions")
            if not ws:
                print("❌ Creating predictions worksheet...")
                try:
                    ws = self.spreadsheet.add_worksheet(title="predictions", rows=1000, cols=10)
                    # Add headers
                    headers = [
                        "Timestamp", "Location", "Rainfall", "Water Level", 
                        "Humidity", "Temp Min", "Temp Max", "Risk Level", 
                        "Status", "Message"
                    ]
                    ws.append_row(headers)
                    print("✅ Created predictions worksheet with headers")
                except Exception as e:
                    print(f"❌ Failed to create predictions worksheet: {e}")
                    return False
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [
                timestamp,
                prediction_data.get('location', ''),
                prediction_data.get('rainfall', 0),
                prediction_data.get('water_level', 0),
                prediction_data.get('humidity', 0),
                prediction_data.get('temp_min', 0),
                prediction_data.get('temp_max', 0),
                prediction_data.get('risk_level', 0),
                prediction_data.get('status', ''),
                prediction_data.get('message', '')
            ]
            
            ws.append_row(row)
            print(f"✅ Prediction saved to Google Sheets")
            return True
            
        except Exception as e:
            print(f"❌ Error saving prediction: {e}")
            return False
    
    def get_predictions(self, limit=100):
        """Get recent predictions from Google Sheets"""
        try:
            ws = self.get_worksheet("predictions")
            if not ws:
                return []
            
            all_data = ws.get_all_values()
            if len(all_data) <= 1:
                return []
            
            headers = all_data[0]
            rows = all_data[1:]
            
            recent_rows = rows[-limit:] if len(rows) > limit else rows
            recent_rows.reverse()
            
            predictions = []
            for row in recent_rows:
                if len(row) >= len(headers):
                    prediction = {headers[i]: row[i] for i in range(min(len(headers), len(row)))}
                    predictions.append(prediction)
            
            return predictions
            
        except Exception as e:
            print(f"❌ Error getting predictions: {e}")
            return []
    
    # ========== TAB 3: monthly_stats ==========
    
    def update_statistics(self, stats_data):
        """Update monthly statistics in Google Sheets (TAB 3)"""
        try:
            ws = self.get_worksheet("monthly_stats")
            if not ws:
                print("❌ Creating monthly_stats worksheet...")
                try:
                    ws = self.spreadsheet.add_worksheet(title="monthly_stats", rows=100, cols=6)
                    headers = ["Month", "Total Reports", "Avg Risk", "High Risk Days", "Most Affected Area", "Response Time Avg"]
                    ws.append_row(headers)
                    print("✅ Created monthly_stats worksheet with headers")
                except Exception as e:
                    print(f"❌ Failed to create monthly_stats worksheet: {e}")
                    return False
            
            current_month = datetime.now().strftime("%Y-%m")
            
            # Cek apakah bulan ini sudah ada
            all_data = ws.get_all_values()
            month_exists = False
            
            for i, row in enumerate(all_data):
                if i == 0:  # Skip header
                    continue
                if row and row[0] == current_month:
                    # Update existing row
                    ws.update(f'A{i+1}:F{i+1}', [[
                        current_month,
                        stats_data.get('total_reports', 0),
                        stats_data.get('avg_risk', 0),
                        stats_data.get('high_risk_days', 0),
                        stats_data.get('most_affected_area', ''),
                        stats_data.get('response_time_avg', 0)
                    ]])
                    month_exists = True
                    print(f"✅ Updated existing row for {current_month}")
                    break
            
            if not month_exists:
                # Add new row
                ws.append_row([
                    current_month,
                    stats_data.get('total_reports', 0),
                    stats_data.get('avg_risk', 0),
                    stats_data.get('high_risk_days', 0),
                    stats_data.get('most_affected_area', ''),
                    stats_data.get('response_time_avg', 0)
                ])
                print(f"✅ Added new row for {current_month}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating statistics: {e}")
            return False
    
    def get_statistics(self):
        """Get monthly statistics from Google Sheets"""
        try:
            ws = self.get_worksheet("monthly_stats")
            if not ws:
                return {}
            
            all_data = ws.get_all_values()
            if len(all_data) <= 1:
                return {}
            
            headers = all_data[0]
            latest_row = all_data[-1]  # Get last row (most recent)
            
            if len(latest_row) >= len(headers):
                return {headers[i]: latest_row[i] for i in range(min(len(headers), len(latest_row)))}
            
            return {}
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}
