import requests
from bs4 import BeautifulSoup
import time
import random
import csv

NAMA_FILE = 'dataset_karir_it_freshgraduate.csv'

BIDANG_IT = [
    {"nama": "Data Science & Analytics", "keyword": "data-analyst"},
    {"nama": "Web & Mobile Developer", "keyword": "software-engineer"},
    {"nama": "Cloud & DevOps", "keyword": "devops"},
    {"nama": "Cyber Security", "keyword": "cyber-security"},
    {"nama": "Product & Project Tech", "keyword": "product-manager"}
]

HALAMAN_PER_BIDANG = 15  

print("📝 Membuat file CSV dan menulis header...")
with open(NAMA_FILE, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Bidang_IT', 'Posisi_Pekerjaan', 'Nama_Perusahaan', 
        'Lokasi', 'Gaji', 'Syarat_Deskripsi_Pekerjaan', 'Link_Detail'
    ])

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://id.jobstreet.com/'
}

total_data_terekstrak = 0

try:
    for bidang in BIDANG_IT:
        print(f"\n=======================================================")
        print(f" 📂 MEMPROSES BIDANG: {bidang['nama'].upper()}")
        print(f"=======================================================")
        
        for page in range(1, HALAMAN_PER_BIDANG + 1):
            print(f"🚀 [Halaman {page}/{HALAMAN_PER_BIDANG}] Menarik data...")
            
            url = f"https://id.jobstreet.com/{bidang['keyword']}-jobs?page={page}"
            
            try:
                response = requests.get(url, headers=HEADERS, timeout=15)
                
                if response.status_code == 403:
                    print("⚠️ Terkena limit / 403 Forbidden. Istirahat lebih lama (20 detik)...")
                    time.sleep(20)
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                job_cards = soup.find_all('article')
                
                if not job_cards:
                    job_cards = soup.select('[data-card-type="JobCard"], [id^="job-card"]')
                    
                if not job_cards or len(job_cards) == 0:
                    print(f"ℹ️ Selesai/Tidak ada data lagi di halaman {page}. Lanjut bidang berikutnya.")
                    break
                
                with open(NAMA_FILE, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    for card in job_cards:
                        title_el = card.find('a', {'data-automation': 'jobTitle'}) or card.select_one('[class*="JobTitle"], h1, h2, a')
                        posisi = title_el.text.strip() if title_el else "Tidak Disebutkan"
                        
                        company_el = card.find('a', {'data-automation': 'jobCompany'}) or card.select_one('[class*="JobCompany"], [data-automation="companyName"]')
                        perusahaan = company_el.text.strip() if company_el else "Perusahaan Rahasia"
                        
                        location_el = card.find('a', {'data-automation': 'jobLocation'}) or card.select_one('[class*="JobLocation"], [data-automation="jobLocation"]')
                        lokasi = location_el.text.strip() if location_el else "Indonesia"
                        
                        salary_el = card.find('span', {'data-automation': 'jobSalary'}) or card.select_one('[class*="JobSalary"]')
                        gaji = salary_el.text.strip() if salary_el else "IDR Disembunyikan"
                        
                        link_detail = "https://id.jobstreet.com" + title_el['href'] if (title_el and title_el.has_attr('href')) else "Tidak Ada Link"
                        
                        bullets = card.find_all('li') or card.select('[class*="Bullet"]')
                        if bullets:
                            deskripsi = " | ".join([b.text.strip() for b in bullets])
                        else:
                            deskripsi_el = card.select_one('[class*="Description"], [class*="Teaser"]')
                            deskripsi = deskripsi_el.text.strip() if deskripsi_el else "Lihat detail pada link."
                        
                        writer.writerow([bidang['nama'], posisi, perusahaan, lokasi, gaji, deskripsi, link_detail])
                        total_data_terekstrak += 1
                        
                print(f"✅ Berhasil menyalin {len(job_cards)} loker ke CSV. Total sementara: {total_data_terekstrak} baris.")
                
            except Exception as e:
                print(f"❌ Eror di halaman {page}: {e}")
                
            jeda = random.uniform(4.5, 7.2)
            time.sleep(jeda)
            
except KeyboardInterrupt:
    print("\n🛑 Proses scraping dihentikan manual oleh pengguna.")

finally:
    print(f"\n🏁 SCRAPING SELESAI!")
    print(f"📊 Total seluruh data terkumpul: {total_data_terekstrak} baris.")
    print(f"📂 File dataset mentah kamu siap dicek di: {NAMA_FILE}")