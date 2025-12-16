#!/usr/bin/env python3
"""
Test database secara manual
"""

import os
import sqlite3
from datetime import datetime

print("=" * 60)
print("🧪 MANUAL DATABASE TEST")
print("=" * 60)

# 1. Cek file database
db_file = 'flood_system.db'
print(f"📂 Database file: {os.path.abspath(db_file)}")
print(f"📂 File exists: {os.path.exists(db_file)}")
print(f"📂 File size: {os.path.getsize(db_file) if os.path.exists(db_file) else 0} bytes")

# 2. Hapus jika ada
if os.path.exists(db_file):
    print(f"🗑️ Removing old database...")
    os.remove(db_file)

# 3. Buat database baru
print(f"🔄 Creating new database...")
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Buat tabel SANGAT SEDERHANA
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flood_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        address TEXT,
        flood_height TEXT,
        reporter_name TEXT,
        reporter_phone TEXT,
        photo_path TEXT,
        ip_address TEXT
    )
''')

conn.commit()
print("✅ Table created")

# 4. Test insert
print(f"🧪 Testing insert...")
test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute('''
    INSERT INTO flood_reports 
    (timestamp, address, flood_height, reporter_name, ip_address)
    VALUES (?, ?, ?, ?, ?)
''', (test_time, "Jl. Test Manual", "Setinggi lutut", "Manual User", "192.168.1.100"))

conn.commit()
print("✅ Test insert completed")

# 5. Cek data
cursor.execute('SELECT * FROM flood_reports')
rows = cursor.fetchall()
print(f"📊 Total rows in database: {len(rows)}")

for row in rows:
    print(f"  ID: {row[0]}, Address: {row[2]}, Name: {row[4]}")

# 6. Cek struktur tabel
cursor.execute("PRAGMA table_info(flood_reports)")
columns = cursor.fetchall()
print(f"\n📋 Table structure:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()

print("\n" + "=" * 60)
print("🎯 NEXT STEP:")
print("1. Run: streamlit run app.py")
print("2. Go to 'Lapor Banjir' page")
print("3. Fill form and submit")
print("4. Check terminal for debug output")
print("=" * 60)
