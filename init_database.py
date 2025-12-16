#!/usr/bin/env python3
"""
Script untuk inisialisasi database awal
"""

import sqlite3
import os

def init_database():
    """Initialize database dengan cara yang lebih sederhana"""
    
    db_path = 'flood_system.db'
    
    # Hapus database lama jika ada
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("🗑️ Old database removed")
        except:
            print("⚠️ Could not remove old database")
    
    try:
        # Buat koneksi
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buat tabel sederhana tanpa index
        cursor.execute('''
            CREATE TABLE flood_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                address TEXT NOT NULL,
                flood_height REAL NOT NULL,
                reporter_name TEXT NOT NULL,
                reporter_phone TEXT,
                photo_path TEXT,
                ip_address TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully!")
        print(f"📍 Database location: {os.path.abspath(db_path)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    init_database()
