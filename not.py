import requests
import time
import json
import urllib.parse
import os

# === Konfigurasi ===
LOOPS = 30
DELAY_BETWEEN_ACCOUNTS = 1
DELAY_BETWEEN_LOOPS = 3
DELAY_AFTER_TASK = 15  # tunggu sebelum claim

# Endpoint sesuai bot ini
# Kita bisa mendapatkan URL dasar dari referer
BASE_URL = "https://botsmother.com"
START_TASK_URL = f"{BASE_URL}/api/command/OTk3/ODE0Mg=="
CLAIM_TASK_URL = f"{BASE_URL}/api/command/OTk3/ODE0Nw=="

# === Perbarui Headers agar lebih mirip Browser ===
HEADERS = {
    'accept': 'application/json, text/plain, */*', # Lebih baik meniru header accept browser
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    # Tambahkan referer. Ini seringkali penting.
    'referer': START_TASK_URL # Kita set referer ke URL task sebelumnya
}

DATA_FILE = "data.txt"

def double_encode_if_needed(init_data):
    """Jika belum double-encoded, encode dulu."""
    if "%25" in init_data:
        return init_data
    return urllib.parse.quote(init_data, safe='')

def ensure_data_file_encoded():
    """Baca data.txt, encode bila perlu, simpan kembali."""
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} tidak ditemukan.")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    encoded_lines = [double_encode_if_needed(line) for line in lines]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for line in encoded_lines:
            f.write(line + "\n")
    return encoded_lines

def get_task_id(session, init_data):
    """Gunakan session untuk mengirim request."""
    url = f"{START_TASK_URL}?initData={init_data}"
    try:
        # Gunakan session.get, bukan requests.get
        # Session akan otomatis menangani cookies
        r = session.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status() # Ini akan error jika status code bukan 2xx
        
        # Cek apakah responsnya benar-benar JSON
        if 'application/json' in r.headers.get('Content-Type', ''):
            print("Start task response (JSON):", r.json())
            return r.json().get("task_id")
        else:
            # Jika responsnya bukan JSON (misal: HTML lagi)
            print("Error: Respons dari start task bukan JSON.")
            # print("Response text:", r.text[:300]) # Tampilkan sedikit respons untuk debug
            return None
            
    except json.JSONDecodeError:
        print("Error: Response bukan JSON valid")
        print("Response text:", r.text)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request gagal: {e}")
        return None

def send_reward(session, init_data, task_id):
    """Gunakan session untuk klaim reward."""
    url = f"{CLAIM_TASK_URL}?initData={init_data}&task_id={task_id}"
    try:
        # Gunakan session.get
        r = session.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        print("Claim reward response:", r.json()) # Asumsikan claim juga mengembalikan JSON
    except requests.exceptions.RequestException as e:
        print(f"Claim gagal: {e}")
    except json.JSONDecodeError:
        print("Error: Respons claim bukan JSON valid.")
        print("Response text:", r.text)

# === Eksekusi ===
accounts = ensure_data_file_encoded()

for loop in range(1, LOOPS + 1):
    print(f"\n=== Loop {loop}/{LOOPS} ===")
    for i, init_data in enumerate(accounts, start=1):
        # === Buat Session baru untuk setiap akun agar cookies tidak tercampur ===
        session = requests.Session()
        
        print(f"\n--- Akun {i}/{len(accounts)} ---")
        task_id = get_task_id(session, init_data)
        
        if task_id:
            print(f"Task ID ditemukan: {task_id}. Menunggu {DELAY_AFTER_TASK} detik sebelum claim...")
            time.sleep(DELAY_AFTER_TASK)
            send_reward(session, init_data, task_id)
        else:
            print("Lewati reward, task_id tidak ditemukan.")
        
        time.sleep(DELAY_BETWEEN_ACCOUNTS)
    
    print(f"\nLoop {loop} selesai. Menunggu {DELAY_BETWEEN_LOOPS} detik...")
    time.sleep(DELAY_BETWEEN_LOOPS)
