import streamlit as st

class GoogleSheetsModel:
    def __init__(self):
        self.client = None
        print("ℹ️ GoogleSheetsModel initialized (simplified)")
    
    def save_flood_report(self, report_data):
        """Save report to Google Sheets"""
        try:
            print(f"📊 Would save to Google Sheets: {report_data.get('address')}")
            # Implementasi Google Sheets disini
            return True
        except:
            return False
