import os
import sys
import subprocess
import time
from utils.qr_gen import generate_qr_code

def main():
    print("=" * 60)
    print("🎓 PlacementPrep AI - Next Gen Chatbot Arena (SDG 4)")
    print("=" * 60)
    
    # 1. Generate QR Code
    local_url = "http://localhost:8501"
    qr_path = generate_qr_code(local_url, "static/judge_qr.png")
    print(f"[+] QR Code generated for '{local_url}' at '{qr_path}'")

    # 2. Determine python executable
    python_exe = sys.executable
    if os.path.exists(".venv/Scripts/python.exe"):
        python_exe = os.path.abspath(".venv/Scripts/python.exe")

    print(f"[+] Using Python: {python_exe}")

    # 3. Start FastAPI Evaluation API Server (port 8000)
    print("[+] Launching FastAPI Evaluation Endpoint (POST /chat) on http://0.0.0.0:8000 ...")
    api_process = subprocess.Popen([
        python_exe, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"
    ])

    # Wait 2 seconds for API to bind
    time.sleep(2)

    # 4. Start Streamlit Web Chatbot UI (port 8501)
    print("[+] Launching Streamlit Web App on http://localhost:8501 ...")
    streamlit_cmd = [
        python_exe, "-m", "streamlit", "run", "app.py", 
        "--server.port", "8501", 
        "--server.headless", "true"
    ]
    
    try:
        streamlit_process = subprocess.Popen(streamlit_cmd)
        print("\n" + "*" * 60)
        print("🚀 ALL SYSTEMS RUNNING:")
        print("   👉 Web Chatbot Interface : http://localhost:8501")
        print("   👉 Arena Evaluation API  : http://localhost:8000/chat")
        print("   👉 Interactive API Docs  : http://localhost:8000/docs")
        print("   👉 Judges QR Code Image  : static/judge_qr.png")
        print("*" * 60 + "\n")
        print("Press Ctrl+C to stop both servers.")
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n[!] Shutting down PlacementPrep AI services...")
    finally:
        api_process.terminate()
        try:
            streamlit_process.terminate()
        except Exception:
            pass
        print("[+] All services stopped.")

if __name__ == "__main__":
    main()
