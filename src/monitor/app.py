from flask import Flask, jsonify
import requests
import logging
import time
import threading
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(
    filename='monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

purchases_host = os.getenv("PURCHASES_HOST")
purchases_port = os.getenv("PURCHASES_PORT")
monitor_port = os.getenv("MONITOR_PORT")

def ping_service():
    try:
        response = requests.get(f"http://{purchases_host}:{purchases_port}/ping")
        return response.status_code == 200
    except requests.RequestException:
        return False

def monitor_status():
    while True:
        try:
            response = ping_service()
            status = "healthy" if response else "unhealthy"
            log_message = f"Service status: {status}"
            print(f"{log_message}")
            logging.info(log_message)
        except Exception as e:
            print(f"Request failed: {e}")
        
        time.sleep(2)

thread = threading.Thread(target=monitor_status, daemon=True)
thread.start()

@app.route('/')
def index():
    return jsonify({"message": "OK"})

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=monitor_port)
