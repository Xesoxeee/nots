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
START_TASK_URL = "https://botsmother.com/api/command/OTk3/ODE0Mg==?initData={init_data}"
CLAIM_TASK_URL = "https://botsmother.com/api/command/OTk3/ODE0Nw==?initData={init_data}&task_id={task_id}"

HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
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

def get_task_id(init_data):
    url = START_TASK_URL.format(init_data=init_data)
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print("Start task response:", r.text)
        data = json.loads(r.text)
        return data.get("task_id")
    except json.JSONDecodeError:
        print("Error: Response bukan JSON valid")
        return None
    except Exception as e:
        print("Request gagal:", e)
        return None

def send_reward(init_data, task_id):
    url = CLAIM_TASK_URL.format(init_data=init_data, task_id=task_id)
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print("Claim reward response:", r.text)
    except Exception as e:
        print("Claim gagal:", e)

# === Eksekusi ===
accounts = ensure_data_file_encoded()

for loop in range(1, LOOPS + 1):
    print(f"\n=== Loop {loop}/{LOOPS} ===")
    for i, init_data in enumerate(accounts, start=1):
        print(f"\n--- Akun {i}/{len(accounts)} ---")
        task_id = get_task_id(init_data)
        time.sleep(DELAY_AFTER_TASK)
        if task_id:
            send_reward(init_data, task_id)
        else:
            print("Lewati reward, task_id tidak ditemukan.")
        time.sleep(DELAY_BETWEEN_ACCOUNTS)
    time.sleep(DELAY_BETWEEN_LOOPS)
