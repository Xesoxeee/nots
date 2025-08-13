import requests
import time
import json
import urllib.parse
import os

LOOPS = 30
DELAY_BETWEEN_ACCOUNTS = 1
DELAY_BETWEEN_LOOPS = 3

HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

DATA_FILE = "data.txt"

def double_encode_if_needed(init_data):
    """
    If init_data is not double-encoded, double-encode it.
    Example: 
      once-encoded  -> user=%7B%22id%22...
      double-encoded -> user%3D%257B%2522id%2522...
    """
    # If it's already double encoded, it will contain "%25" frequently
    if "%25" in init_data:
        return init_data  # already double-encoded
    # Double encode
    return urllib.parse.quote(init_data, safe='')

def ensure_data_file_encoded():
    """Read data.txt, double-encode any entries if needed, and rewrite the file."""
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found")
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    encoded_lines = [double_encode_if_needed(line) for line in lines]

    # Overwrite file with corrected values
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for line in encoded_lines:
            f.write(line + "\n")

    return encoded_lines

def get_task_id(init_data):
    url = f"https://botsmother.com/api/command/OTk3/ODE0Nw==?initData={init_data}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print("First response raw:", r.text)
        data = json.loads(r.text)
        return data.get("task_id")
    except json.JSONDecodeError:
        print("Error: Response was not valid JSON")
        return None
    except Exception as e:
        print("Request failed:", e)
        return None

def send_reward(init_data, task_id):
    url = f"https://botsmother.com/api/command/OTk3/ODE0Nw==?initData={init_data}&task_id={task_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print("Second response raw:", r.text)
    except Exception as e:
        print("Reward request failed:", e)

# Step 1: Ensure all lines in data.txt are double-encoded
accounts = ensure_data_file_encoded()

# Step 2: Main loop
for loop in range(1, LOOPS + 1):
    print(f"\n=== Loop {loop}/{LOOPS} ===")
    for i, init_data in enumerate(accounts, start=1):
        print(f"\n--- Account {i}/{len(accounts)} ---")
        task_id = get_task_id(init_data)
        time.sleep(15)
        if task_id:
            send_reward(init_data, task_id)
        else:
            print("Skipping reward, no task_id found.")
        time.sleep(DELAY_BETWEEN_ACCOUNTS)
    time.sleep(DELAY_BETWEEN_LOOPS)
