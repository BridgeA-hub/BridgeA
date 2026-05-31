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

print("--- DAFTAR GURU ---")
for doc in db.collection('guru').stream():
    print(f"ID: {doc.id} => {doc.to_dict()}")

print("\n--- DAFTAR KELAS ---")
for doc in db.collection('kelas').stream():
    print(f"ID: {doc.id} => {doc.to_dict()}")
