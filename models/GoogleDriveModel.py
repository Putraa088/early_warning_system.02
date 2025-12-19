# models/GoogleDriveModel.py
import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import mimetypes
import streamlit as st

class GoogleDriveModel:
    def __init__(self):
        """Initialize Google Drive connection"""
        self.service = None
        self.folder_id = None
        self.setup_connection()
    
    def setup_connection(self):
        """Setup Google Drive connection"""
        try:
            print("🔄 Setting up Google Drive connection...")
            
            # Scope untuk Google Drive
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            # Coba dari Streamlit Secrets (Cloud)
            if 'GOOGLE_SHEETS' in st.secrets:
                print("🔑 Using Streamlit Secrets for Google Drive")
                
                # Bangun credentials dari secrets
                credentials_dict = {
                    "type": "service_account",
                    "project_id": st.secrets['GOOGLE_SHEETS']['project_id'],
                    "private_key_id": st.secrets['GOOGLE_SHEETS']['private_key_id'],
                    "private_key": st.secrets['GOOGLE_SHEETS']['private_key'].replace('\\n', '\n'),
                    "client_email": st.secrets['GOOGLE_SHEETS']['client_email'],
                    "client_id": st.secrets['GOOGLE_SHEETS']['client_id'],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": st.secrets['GOOGLE_SHEETS']['client_x509_cert_url']
                }
                
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_dict, 
                    scopes=SCOPES
                )
                
            # Fallback ke credentials.json (Local)
            elif os.path.exists('credentials.json'):
                print("🔑 Using credentials.json for Google Drive")
                credentials = service_account.Credentials.from_service_account_file(
                    'credentials.json',
                    scopes=SCOPES
                )
            
            else:
                print("❌ No Google credentials found")
                self.service = None
                return
            
            # Build service
            self.service = build('drive', 'v3', credentials=credentials)
            print("✅ Google Drive API authorized")
            
            # Cari atau buat folder 'flood_report_photos'
            self.folder_id = self._get_or_create_folder('flood_report_photos')
            print(f"✅ Using folder ID: {self.folder_id}")
            
        except Exception as e:
            print(f"❌ Google Drive connection failed: {e}")
            self.service = None
    
    def _get_or_create_folder(self, folder_name):
        """Cari atau buat folder di Google Drive"""
        try:
            # Cari folder yang sudah ada
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                # Folder sudah ada
                return folders[0]['id']
            else:
                # Buat folder baru
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                print(f"✅ Created folder: {folder_name}")
                return folder.get('id')
                
        except Exception as e:
            print(f"❌ Error getting/creating folder: {e}")
            return None
    
    def upload_photo(self, file_bytes, filename, mime_type=None):
        """Upload photo ke Google Drive dan return shareable link"""
        if not self.service or not self.folder_id:
            print("❌ Google Drive not available")
            return None
        
        try:
            # Tentukan mime type
            if not mime_type:
                mime_type = mimetypes.guess_type(filename)[0] or 'image/jpeg'
            
            print(f"📤 Uploading {filename} ({len(file_bytes)} bytes) to Google Drive...")
            
            # File metadata
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            # Create media upload
            media = MediaIoBaseUpload(
                io.BytesIO(file_bytes),
                mimetype=mime_type,
                resumable=True
            )
            
            # Upload file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink, webContentLink'
            ).execute()
            
            # Buat file bisa diakses publik (view only)
            self.service.permissions().create(
                fileId=file['id'],
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
            
            print(f"✅ Uploaded to Google Drive: {file['id']}")
            
            # Return URL yang bisa dilihat langsung
            return {
                'file_id': file['id'],
                'view_url': file['webViewLink'],  # Link ke Google Drive UI
                'direct_url': f"https://drive.google.com/uc?id={file['id']}",  # Direct image link
                'filename': filename
            }
            
        except Exception as e:
            print(f"❌ Error uploading to Google Drive: {e}")
            return None
    
    def delete_file(self, file_id):
        """Delete file dari Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"✅ Deleted file: {file_id}")
            return True
        except Exception as e:
            print(f"❌ Error deleting file: {e}")
            return False