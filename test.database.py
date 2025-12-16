import sqlite3
import os

print("=== TEST DATABASE ===")

# Cek file database
db_path = 'flood_system.db'
print(f"Database file exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Cek tabel
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        # Cek struktur tabel flood_reports
        cursor.execute("PRAGMA table_info(flood_reports)")
        columns = cursor.fetchall()
        print("Columns in flood_reports:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Coba insert test data
        test_data = (
            '2024-01-15 10:00:00',
            'Jl. Test',
            50.0,
            'Test User',
            '081234567890',
            None,
            '192.168.1.1'
        )
        
        cursor.execute('''
            INSERT INTO flood_reports 
            (timestamp, address, flood_height, reporter_name, reporter_phone, photo_path, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', test_data)
        conn.commit()
        
        print("✅ Test insert successful!")
        
        # Cek total data
        cursor.execute("SELECT COUNT(*) FROM flood_reports")
        count = cursor.fetchone()[0]
        print(f"Total reports in database: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ Database file not found!")
