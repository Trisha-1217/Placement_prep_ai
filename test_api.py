import threading
import time
import uvicorn
import requests
from api import app

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="warning")

def test_api():
    print("=== Testing FastAPI Endpoints ===")
    
    # 1. Start server in a thread
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1.5)
    
    base_url = "http://127.0.0.1:8001"
    
    # 2. Test GET /
    res_root = requests.get(f"{base_url}/")
    print(f"[GET /] Status: {res_root.status_code}")
    print(f"Data: {res_root.json()}")
    assert res_root.status_code == 200
    
    # 3. Test GET /health
    res_health = requests.get(f"{base_url}/health")
    print(f"\n[GET /health] Status: {res_health.status_code}")
    print(f"Data: {res_health.json()}")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
    
    # 4. Test POST /chat (Standardized Arena Prompt)
    payload = {
        "message": "Teach me the basics of linear regression as if I am a beginner, then give me three practice questions."
    }
    res_chat = requests.post(f"{base_url}/chat", json=payload)
    print(f"\n[POST /chat] Status: {res_chat.status_code}")
    reply = res_chat.json()
    print(f"Response: {reply['response'][:160]}...")
    assert res_chat.status_code == 200
    assert "response" in reply
    assert len(reply["response"]) > 30

    print("\n[+] All API endpoint tests PASSED successfully!")

if __name__ == "__main__":
    test_api()
