import httpx
import json
import time
import subprocess
import os

SERVER_URL = "http://127.0.0.1:7842"
PYTHON_EXE = r"c:\Users\Dronzer\Desktop\LogAnalyser\venv\Scripts\python.exe"

TRACEBACK = """  File "c:/Users/Dronzer/Desktop/test.py", line 23
    print(f"🚨 ChromeDriver failed to start: {e}"
         ^
SyntaxError: '(' was never closed"""

def test_server():
    print(f"Checking server at {SERVER_URL}...")
    try:
        resp = httpx.get(f"{SERVER_URL}/health", timeout=5)
        print(f"Health check: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Server not running, attempting to start it...")
        # Start server in background
        subprocess.Popen(
            [PYTHON_EXE, "-m", "snapfix", "server"],
            cwd=r"c:\Users\Dronzer\Desktop\LogAnalyser\snapfix-backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(5)  # Wait for startup

    print("Sending SyntaxError traceback for analysis...")
    try:
        payload = {
            "traceback": TRACEBACK,
            "context": "python",
            "project_path": r"c:\Users\Dronzer\Desktop\LogAnalyser"
        }
        resp = httpx.post(f"{SERVER_URL}/analyze", json=payload, timeout=45)
        print(f"Analysis status: {resp.status_code}")
        if resp.status_code == 200:
            result = resp.json()
            print("\n--- SNAPFIX ANALYSIS RESULT ---")
            
            # Display based on new 0.2.0 schema
            what = result.get('what_happened', {})
            print(f"Headline: {what.get('headline', 'N/A')}")
            print(f"Detail:   {what.get('detail', 'N/A')}")
            
            fix = result.get('fix', {})
            print(f"\nFix Explanation: {fix.get('explanation', 'N/A')}")
            print(f"Proposed Code:\n{fix.get('code', 'N/A')}")
            
            meta = result.get('meta', {})
            print(f"\nSeverity: {meta.get('severity', 'N/A')} | Category: {meta.get('category', 'N/A')}")
            print("----------------------------------\n")
            return True
        else:
            print(f"Error detail: {resp.text}")
            return False
    except Exception as e:
        print(f"Analysis request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    if success:
        print("✅ SUCCESS: Snapfix Engine is working perfectly with Gemma 3!")
        exit(0)
    else:
        print("❌ FAILURE: Pipeline check failed.")
        exit(1)
