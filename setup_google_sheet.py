#!/usr/bin/env python3
"""
Setup Google Sheets for Flood Warning System
"""

import os
import json

def setup_google_sheets():
    print("=" * 60)
    print("🔧 SETUP GOOGLE SHEETS FOR FLOOD WARNING SYSTEM")
    print("=" * 60)
    
    # 1. Check credentials.json
    print("\n1. Checking credentials.json...")
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
        
        print(f"✅ credentials.json found")
        print(f"   Project ID: {creds.get('project_id')}")
        print(f"   Client Email: {creds.get('client_email')}")
        
        # Check private key format
        private_key = creds.get('private_key', '')
        if '\\n' in private_key:
            print("⚠️ Private key has \\n instead of actual newlines")
            print("   Fixing automatically...")
            
            # Fix newlines
            creds['private_key'] = private_key.replace('\\n', '\n')
            
            # Save fixed version
            with open('credentials.json', 'w') as f:
                json.dump(creds, f, indent=2)
            
            print("✅ Private key format fixed")
    else:
        print("❌ credentials.json not found")
        print("   Please download from Google Cloud Console")
        return False
    
    # 2. Check spreadsheet access
    print("\n2. Testing Google Sheets connection...")
    try:
        from models.GoogleSheetsModel import GoogleSheetsModel
        
        model = GoogleSheetsModel()
        if model.client:
            print("✅ Google Sheets connection successful!")
            print(f"   Spreadsheet: {model.spreadsheet.title if model.spreadsheet else 'N/A'}")
            
            # Test write
            test_data = {
                'address': 'Setup Test',
                'flood_height': 'Test',
                'reporter_name': 'Setup Script',
                'reporter_phone': '',
                'ip_address': '127.0.0.1',
                'photo_url': ''
            }
            
            if model.save_flood_report(test_data):
                print("✅ Test write successful!")
            else:
                print("⚠️ Test write failed (but connection OK)")
        else:
            print("❌ Google Sheets connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 3. Setup Streamlit secrets
    print("\n3. Setting up Streamlit secrets...")
    secrets_content = """[GOOGLE_SHEETS]
project_id = "flood-warning-system-481323"
private_key_id = "fe14d49f13f2eb2e02ac804f33e0141017badde4"
private_key = \"\"\"
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDtLqRkg7rnf08X
tKE6aFO2mTuaxZ9xEno6FekEC/TdxPsUrTtzolPVjYsEIjdnaEZPTk/1YYb8b0NL
ZRSRGY5iZ2jbrHFHpREok+w5OYokiOZ0z5hb0PvlIJnWc7uPU/eKHo/fGQrb8FvJ
t4nz1c0vBqwhR/ipt736VXwma6XmnnRVwBs2QBouCExLsdXMqBmXZ/8Z0lGMFHiZ
szelQEk2i4r98AS19t/Nfo9cqCeGHrCRBDKnrOQjb6kbJM1wr9FY5w0tgHQIJzwn
j+rwM9ZtCdl8mWFwGesM7aDsFQF3tsMesSbBheHBPsNQzbfWiN9cLcF1ab9S4fL3
w0wOIyfVAgMBAAECggEAAft6kMOAF6i6/L/7+/y8vGE1/BJsRXnpzxv5RVkjPApG
LfNPtKT17eo/r/JoQ6M9uTJ2nR6qTehRJ+tpm1fbFov2NqXPkZF53fy0g/rs4mbJ
hE7q31OVE2JtHrt7ZRSG1F7yhWMUceeloL85tjHChALag/GxzJtWSWYXAkwyiAWl
ZKs1PsnbdUb/HFXyTbpSWdjPOwfTqC9KJFOalWOcAMlVDHjXMCs2zuN/DH/7csu9
9udMBocrH2BSYVgqa4/7auZMDeWjo464L9KOTmn7W8dyYIIL8RBHHEaPE28Mp3pY
es9zas/9nSy3po4/CAWyRO2/Q9WB9K+JDOmqhVhe6QKBgQD/GUSeyNblNoGlT3B/
8WJPbZorS6/izsHODtDrCftF+uNHjt43lzUvSQJFqUipISAQKIr5fI5U+9EdeKuE
c4Lo6YAr2jKZTzLZqw5ZVM8T0mNx4kJ6plGQ7Oc/S5alCxh5mBPXAH05JqAbY6jh
4mglvjKDK0YL7+mxhjHnM+tHrQKBgQDuBStBinTkhFdiPnpJ+Vvz6e75YtjZ/qmP
f298ZeZN8Yox/8VtxeLENzpNNStoEIvENeAxp9DKBaT3/GubmzDj0RkV0Dv1+LMS
qfX/62mKSARjpsKnLMMDSWyv6guU2JR+CBuCzr9RAyetDn3x/Krt51mtfCMZELem
EYouSDeFyQKBgG66ahW+OcEuoqG91KhEf5bYjUXjyYnakzc9KSQMphwfJc5mzkA1
CynmN+1C6L45GbDJ2GEo1qM+1utC+Lg6Z4Vv7WmbgcEYJoti+4x9CpGhDfdd7dtN
HDSbEFliFxa2tT36bAo0NSa8hFy/Kow5+VkAsO5Mt0/xKHAdPsYLvEHVAoGAJgSl
WB6pdSa+Xm7kUZSG33rqNONZB9jpdIZCZHhSRPjjvgDApDwLcJPxuAtaF5EtAfYp
DUVk0B/+ra2f8objVEA95YIRUcSbtct4A5yyiufd65zjUpiPvaKovaCAoRHHBip9
WnNzk5kRaU77Rv/4va9KX6+IW6ST8O60R5g5ZiECgYBq6Z5n0nfbX+2cq9/KDREA
1QLgeQ0Nxcq20lZ2Hfl74hUzfx3KwTU7rohfEKZejMxOLIWePs3fGZFVNPjM6sI3
W6w70c4XIKDVZh+RrAcFZWJXfqjhW9kj/SAHQJZrKB2nc+XVapOihbUHHDjlaumP
yXClNdY/GSJueMBGHT3dSA==
-----END PRIVATE KEY-----
\"\"\"
client_email = "flood-sheets-access@flood-warning-system-481323.iam.gserviceaccount.com"
client_id = "110784498522048110065"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/flood-sheets-access%40flood-warning-system-481323.iam.gserviceaccount.com"
SPREADSHEET_ID = "1wdys3GzfDfl0ohCQjUHRyJVbKQcM0VSIMgCryHB0-mc"

[SYSTEM]
admin_email = "tyarawahyusaputra@gmail.com"
admin_phone = "085156959561"
max_reports_per_day = 10
upload_folder = "uploads"
"""
    
    # Create .streamlit folder if not exists
    if not os.path.exists('.streamlit'):
        os.makedirs('.streamlit')
    
    # Write secrets.toml
    with open('.streamlit/secrets.toml', 'w') as f:
        f.write(secrets_content)
    
    print("✅ Streamlit secrets created: .streamlit/secrets.toml")
    print("⚠️ IMPORTANT: Don't commit secrets.toml to GitHub!")
    
    print("\n" + "=" * 60)
    print(" SETUP COMPLETE!")
    print("\n Next Steps:")
    print("1. Share your Google Sheet with this email:")
    print("   flood-sheets-access@flood-warning-system-481323.iam.gserviceaccount.com")
    print("   Set permission to 'Editor'")
    print("\n2. Test the system:")
    print("   python test_google_sheets_final.py")
    print("\n3. Deploy to Streamlit Cloud:")
    print("   - Push to GitHub")
    print("   - Add secrets in Streamlit Cloud dashboard")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    setup_google_sheets()