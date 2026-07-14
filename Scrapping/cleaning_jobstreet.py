import pandas as pd
import re
import os

print("📂 Memuat dataset mentah JobStreet...")
nama_file_mentah = 'dataset_karir_it_freshgraduate.csv'

if not os.path.exists(nama_file_mentah):
    print(f"❌ Eror: File {nama_file_mentah} tidak ditemukan di folder ini!")
    exit()

df = pd.read_csv(nama_file_mentah, encoding='utf-8')
print(f"✅ Data awal berhasil dimuat: {df.shape[0]} baris.")

print("🧹 Menghapus data duplikat dan baris kosong...")
df.drop_duplicates(subset=['Posisi_Pekerjaan', 'Nama_Perusahaan'], inplace=True)
df.dropna(subset=['Posisi_Pekerjaan'], inplace=True)

df['Gaji'] = df['Gaji'].str.replace('Â', '', case=False, regex=False)
df['Gaji'] = df['Gaji'].str.replace('â€“', '-', regex=False)

print("⚙️ Memproses ekstraksi kata kunci (Skill Matrix)...")
df['Deskripsi_Lower'] = df['Syarat_Deskripsi_Pekerjaan'].str.lower().fillna('')

df['Skill_Python'] = df['Deskripsi_Lower'].str.contains('python').astype(int)
df['Skill_SQL'] = df['Deskripsi_Lower'].str.contains('sql|database|mysql|postgresql|oracle').astype(int)
df['Skill_Javascript'] = df['Deskripsi_Lower'].str.contains('javascript|js|typescript|ts').astype(int)
df['Skill_PHP'] = df['Deskripsi_Lower'].str.contains('php|laravel|ci|codeigniter').astype(int)
df['Skill_Java_Kotlin'] = df['Deskripsi_Lower'].str.contains('java|kotlin|android').astype(int)
df['Skill_Excel'] = df['Deskripsi_Lower'].str.contains('excel|spreadsheet').astype(int)
df['Skill_Cloud_AWS_GCP'] = df['Deskripsi_Lower'].str.contains('aws|gcp|azure|cloud').astype(int)
df['Skill_Docker_K8s'] = df['Deskripsi_Lower'].str.contains('docker|kubernetes|k8s|devops').astype(int)
df['Skill_Git'] = df['Deskripsi_Lower'].str.contains('git|github|gitlab').astype(int)
df['Skill_English'] = df['Deskripsi_Lower'].str.contains('english|inggris|toeic|toefl').astype(int)
df['Skill_Agile_Scrum'] = df['Deskripsi_Lower'].str.contains('agile|scrum|jira').astype(int)
df['Skill_Networking_Security'] = df['Deskripsi_Lower'].str.contains('network|ccna|security|cyber|firewall').astype(int)

print("💰 Mengonversi kolom gaji teks menjadi format angka numerik...")

def bersihkan_gaji(teks):
    if pd.isna(teks) or 'disembunyikan' in str(teks).lower():
        return None
    angka_saja = re.findall(r'\d+', str(teks).replace('.', ''))
    if len(angka_saja) == 2:  # Jika range gaji
        return (float(angka_saja[0]) + float(angka_saja[1])) / 2
    elif len(angka_saja) == 1:
        return float(angka_saja[0])
    return None

df['Gaji_Clean'] = df['Gaji'].apply(bersihkan_gaji)

df.drop(columns=['Deskripsi_Lower'], inplace=True)

NAMA_FILE_BERSIH = 'dataset_tech_skills_clean.csv'
df.to_csv(NAMA_FILE_BERSIH, index=False, sep=';', encoding='utf-8-sig')

print("\n=======================================================")
print("🎉 PROSES CLEANING SELESAI TOTAL!")
print(f"📊 Jumlah data bersih setelah di-filter: {df.shape[0]} baris.")
print(f"📁 File CSV siap dikumpul ke dosen: {NAMA_FILE_BERSIH}")
print("=======================================================")