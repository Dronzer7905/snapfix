import requests
import json

API_KEY = "AIzaSyAHQkiSg3YAEFPcwVrcf2bhfSqQBRTTDFo"
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print(f"Fetching available models for key: {API_KEY[:8]}...")
try:
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        models = data.get("models", [])
        print(f"Found {len(models)} models:")
        for m in models:
            name = m.get("name", "unknown")
            methods = m.get("supportedGenerationMethods", [])
            if "generateContent" in methods:
              print(f" - {name} (Supports generateContent)")
    else:
        print(f"❌ Failed to list models: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Request failed: {e}")
