from flask import Flask
import random
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

purchases_port = os.getenv("PURCHASES_PORT")

@app.route('/ping')
def health_check():
    if random.random() < 0.9:
        return {"status": "echo"}, 200
    return {"status": "INTERNAL SERVER ERROR"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=purchases_port)
