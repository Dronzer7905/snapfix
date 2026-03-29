import http.client
import json

conn = http.client.HTTPConnection("127.0.0.1", 7842)
try:
    conn.request("GET", "/health")
    resp = conn.getresponse()
    print("STATUS:", resp.status)
    print("BODY:", resp.read().decode())
except Exception as e:
    print("ERROR:", e)
finally:
    conn.close()
