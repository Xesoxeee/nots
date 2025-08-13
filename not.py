import requests
import time
import json
import urllib.parse
import os

LOOPS = 30
DELAY_BETWEEN_ACCOUNTS = 1
DELAY_BETWEEN_LOOPS = 3
DATA_FILE = "data.txt"

# Cookie langsung dari DevTools
COOKIES = {
    'XSRF-TOKEN': 'eyJpdiI6IkllZTN2WW4zVGd5OTBJeXh1WlllZHc9PSIsInZhbHVlIjoiRzBiRkl5NGRpc2hJNWhqb1ljMGRCRXBDZDI4bVpSNnZ3a2E1VXNqNHlDT2tid05TVmFBQUxXMGFvS1VOeTl2YWxBalBCVXE5ckg4SWkreURZSDhIaFlXM2J3MDkwQkxRdmJwWjJkKzlweGZOQU5TUERIZmRzaU5abHdoM0xQNTkiLCJtYWMiOiJmMDA3ZTYwZDUyYWVjNGE1MjZhM2IwYzY5ODJlYmFhNWVkNGQ5ZjhkMzBkYzY2NDA2NTU1YTI4NjZhZGUxZjcxIiwidGFnIjoiIn0%3D',
    'bots_mother_session': 'eyJpdiI6IkJjeFVvVlg0ckJsSjdobGFEaXpRUnc9PSIsInZhbHVlIjoiWEd3eWtENDNuSThUdXZaNVdGbmVKQUY0dWZFNERRZFNlRFlWQzBaQnM0bVhnekl1TGg4ZExubm1PYkRGTFpuTkpacmh4elZWay9OajI2VlJVWFIvYUVkMUk1UUVNZnQ1am81M2ZNZkdXZWd1V2U2UytMOHVSQlV0MlNmRWNTMFMiLCJtYWMiOiIxODk2NDJjOTU4NjY0ZmUyNjgxMGZlMmFlOWNjY2IyZjNmY2ExNmI2ZTZhNDJmN2VlOTI5Y2UyNjEwMjQ2OTIzIiwidGFnIjoiIn0%3D'
}

# Header copy-paste dari browser
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'origin': 'https://botsmother.com',
    'referer': 'https://botsmother.com/api/command/OTk3/ODE0Mg==',
    'sec-ch-ua': '"Chromium";v="138", "Microsoft Edge";v="138", "Microsoft Edge WebView2";v="138", "Not)A;Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
}

def double_encode_if_needed(init_data):
    if "%25" in init_data:
        return init_data
    return urllib.parse.quote(init_data, safe='')

def ensure_data_file_encoded():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    encoded_lines = [double_encode_if_needed(line) for line in lines]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for line in encoded_lines:
            f.write(line + "\n")
    return encoded_lines

def get_task_id(init_data):
    url = f"https://botsmother.com/api/command/OTk3/ODE0Mg==?initData={init_data}"
    try:
        r = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=15)
        print("First response raw:", r.text)
        data = json.loads(r.text)
        return data.get("task_id")
    except json.JSONDecodeError:
        print("Error: Response was not valid JSON (mungkin cookies/initData expired)")
        return None
    except Exception as e:
        print("Request failed:", e)
        return None

def send_reward(init_data, task_id):
    url = f"https://botsmother.com/api/command/OTk3/ODE0Nw==?initData={init_data}&task_id={task_id}"
    try:
        r = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=15)
        print("Second response raw:", r.text)
    except Exception as e:
        print("Reward request failed:", e)

accounts = ensure_data_file_encoded()

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
