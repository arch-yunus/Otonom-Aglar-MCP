import os
import sys
import threading
import time
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mcp-secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Ajanın düşünce zincirini simüle eden veya loglardan çeken yapı
logs = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "connected_servers": ["SQLite", "GitHub", "Web", "Semantic Memory", "File System"],
        "active_agent": "Autonomous Brain v2"
    })

def mock_log_generator():
    """Gerçek zamanlı log akışını simüle eder (İleride gerçek loglara bağlanabilir)"""
    while True:
        time.sleep(5)
        new_log = {
            "type": "Thought",
            "message": "Bellekteki geçmiş verileri analiz ediyorum...",
            "time": time.strftime("%H:%M:%S")
        }
        socketio.emit('new_log', new_log)

@socketio.on('connect')
def handle_connect():
    print("Dashboard connected!")
    emit('server_status', {"message": "Bağlantı kuruldu."})

if __name__ == '__main__':
    # Log simülasyonunu başlat
    threading.Thread(target=mock_log_generator, daemon=True).start()
    socketio.run(app, debug=True, port=5000)
