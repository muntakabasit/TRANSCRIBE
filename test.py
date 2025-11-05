import requests
import json
import os

url = os.getenv("REPLIT_DEV_DOMAIN", "localhost:5000")
base_url = f"https://{url}" if not url.startswith("localhost") else f"http://{url}"
endpoint = f"{base_url}/transcribe"

payload = {"url": "https://www.instagram.com/reel/YOUR_JAYZ_CLIP_ID/"}

print(f"Testing endpoint: {endpoint}")
print(f"Payload: {payload}\n")

response = requests.post(endpoint, json=payload)
if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, indent=2))
    if result['segments']:
        avg_len = sum(s['end'] - s['start'] for s in result['segments']) / len(result['segments'])
        print(f"\nAvg segment: {avg_len:.2f}s — feed to AutoCut beats")
else:
    print(f"Error: {response.text}")
