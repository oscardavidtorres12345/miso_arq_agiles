from flask import Flask, jsonify
import requests
import logging
import time
import threading

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(
    filename='monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def ping_service():
    try:
        response = requests.get('http://ec2-54-87-174-191.compute-1.amazonaws.com:5000/ping')
        return response.status_code == 200
    except requests.RequestException:
        return False

def monitor_status():
    while True:
        try:
            response = ping_service()
            status = "healthy" if response else "unhealthy"
            log_message = f"Service status: {status}"
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

    app.run(host='0.0.0.0', port=5001)
