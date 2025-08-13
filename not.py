import requests
import time
import json
import urllib.parse
import os

# === Konfigurasi ===
LOOPS = 30
DELAY_BETWEEN_ACCOUNTS = 2 # Sedikit jeda antar akun
DELAY_BETWEEN_LOOPS = 5  # Jeda antar putaran
DELAY_AFTER_TASK = 15    # Tunggu sebelum klaim

# URL Endpoint dari cURL (sudah benar)
BASE_URL = "https://botsmother.com"
START_TASK_URL = f"{BASE_URL}/api/command/OTk3/ODE0Mg=="
CLAIM_TASK_URL = f"{BASE_URL}/api/command/OTk3/ODE0Nw=="

# === HEADERS LENGKAP DARI cURL ===
# Ini adalah kunci utamanya. Kita meniru semua header dari browser.
# Cookie tidak perlu dimasukkan di sini karena akan di-handle oleh requests.Session
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': START_TASK_URL, # Referer di-set ke URL start task
    'sec-ch-ua': '"Chromium";v="138", "Microsoft Edge";v="138", "Microsoft Edge WebView2";v="138", "Not)A;Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
}

DATA_FILE = "data.txt"

def read_init_data():
    """Membaca initData dari file data.txt."""
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} tidak ditemukan.")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        # Menghapus spasi dan memastikan tidak ada baris kosong
        return [line.strip() for line in f if line.strip()]

def get_task_id(session, init_data):
    """Memulai task dan mendapatkan task_id."""
    url = f"{START_TASK_URL}?initData={urllib.parse.quote(init_data)}"
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status() # Error jika status bukan 2xx (misal: 403, 500)
        
        data = r.json()
        print("Start task response (JSON):", data)
        return data.get("task_id")
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error saat start task: {http_err}")
        print(f"Response body: {r.text}")
    except Exception as e:
        print(f"Request gagal saat start task: {e}")
    return None

def send_reward(session, init_data, task_id):
    """Menggunakan task_id untuk klaim hadiah."""
    url = f"{CLAIM_TASK_URL}?initData={urllib.parse.quote(init_data)}&task_id={task_id}"
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        
        print("Claim reward response:", r.json())
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error saat klaim: {http_err}")
        print(f"Response body: {r.text}")
    except Exception as e:
        print(f"Claim gagal: {e}")

# === Eksekusi Utama ===
accounts = read_init_data()
if not accounts:
    print("Tidak ada akun di data.txt untuk diproses.")
else:
    for loop in range(1, LOOPS + 1):
        print(f"\n{'='*10} Loop {loop}/{LOOPS} {'='*10}")
        for i, init_data in enumerate(accounts, start=1):
            session = requests.Session()
            
            print(f"\n--- Akun {i}/{len(accounts)} ---")
            task_id = get_task_id(session, init_data)
            
            if task_id:
                print(f"Task ID ditemukan: {task_id}. Menunggu {DELAY_AFTER_TASK} detik...")
                time.sleep(DELAY_AFTER_TASK)
                send_reward(session, init_data, task_id)
            else:
                print("Gagal mendapatkan task_id, lanjut ke akun berikutnya.")
            
            time.sleep(DELAY_BETWEEN_ACCOUNTS)
        
        print(f"\nLoop {loop} selesai. Menunggu {DELAY_BETWEEN_LOOPS} detik...")
        time.sleep(DELAY_BETWEEN_LOOPS)
