# pyrefly: ignore [missing-import]
import firebase_admin
# pyrefly: ignore [missing-import]
from firebase_admin import credentials, firestore
import os

credentials_path = 'firebase-credentials.json'
if os.path.exists(credentials_path):
    cred = credentials.Certificate(credentials_path)
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = firestore.client()

# 1. Perbaiki data guru (Nama diawali huruf kapital)
print("--- MEMPERBAIKI DATA GURU ---")
for doc in db.collection('guru').stream():
    data = doc.to_dict()
    nama_lama = data.get('nama', '')
    if nama_lama:
        nama_baru = nama_lama.title() # Mengubah 'ananta' menjadi 'Ananta' dan 'asep' menjadi 'Asep'
        if nama_lama != nama_baru:
            db.collection('guru').document(doc.id).update({'nama': nama_baru})
            print(f"Update Guru ID {doc.id}: '{nama_lama}' -> '{nama_baru}'")

# 2. Perbaiki data kelas (guru_pengajar dan nama_kelas)
print("\n--- MEMPERBAIKI DATA KELAS ---")
for doc in db.collection('kelas').stream():
    data = doc.to_dict()
    updates = {}
    
    # Perbaiki guru_pengajar
    guru_lama = data.get('guru_pengajar', '')
    if guru_lama:
        guru_baru = guru_lama.title()
        if guru_lama != guru_baru:
            updates['guru_pengajar'] = guru_baru
            print(f"Update Guru Pengajar Kelas ID {doc.id}: '{guru_lama}' -> '{guru_baru}'")
            
    # Perbaiki nama_kelas (Kelas x -> Kelas X)
    kelas_lama = data.get('nama_kelas', '')
    if kelas_lama == 'Kelas x':
        updates['nama_kelas'] = 'Kelas X'
        print(f"Update Nama Kelas ID {doc.id}: 'Kelas x' -> 'Kelas X'")
        
    if updates:
        db.collection('kelas').document(doc.id).update(updates)

print("\nPerbaikan data selesai!")
