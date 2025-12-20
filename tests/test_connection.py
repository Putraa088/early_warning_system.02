import os
import json

def test_google_sheets_connection():
    print("🔗 SIMPLE GOOGLE SHEETS TEST")
    print("=" * 60)
    
    print("\n1. Checking credentials.json...")
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found")
        print("📁 Current directory:", os.getcwd())
        print("📋 Files in directory:")
        for f in os.listdir('.'):
            print(f"  - {f}")
        return False
    
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
        
        print("✅ credentials.json found")
        print(f"   Project ID: {creds.get('project_id')}")
        print(f"   Client Email: {creds.get('client_email')}")
        
        private_key = creds.get('private_key', '')
        if 'BEGIN PRIVATE KEY' in private_key and 'END PRIVATE KEY' in private_key:
            print("✅ Private key format OK")
        else:
            print("❌ Private key format issue")
            return False
        
    except Exception as e:
        print(f"❌ Error reading credentials.json: {e}")
        return False
    
    print("\n2. Testing GoogleSheetsModel...")
    try:
        from models.GoogleSheetsModel import GoogleSheetsModel
        
        print("🔄 Initializing GoogleSheetsModel...")
        model = GoogleSheetsModel()
        
        if model.client:
            print("✅ Google Sheets connected!")
            
            if model.worksheet:
                print(f"✅ Worksheet: {model.worksheet.title}")
                return True
            else:
                print("⚠️ Worksheet not found")
                return True  
        else:
            print("❌ Google Sheets not connected")
            print("ℹ️ System will use SQLite only")
            return False
            
    except ImportError as e:
        print(f"❌ Cannot import GoogleSheetsModel: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_google_sheets_connection()
    if success:
        print("\n✅ Google Sheets connection test PASSED")
        print("🚀 Now run: streamlit run app.py")
    else:
        print("\n❌ Google Sheets connection test FAILED")
        print("ℹ️ System will still work with SQLite database")
