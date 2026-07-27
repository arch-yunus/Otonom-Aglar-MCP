import os
import sys
import threading
import time
import importlib.util
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# Ensure we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mcp-secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store logs for session persistence
logs = [
    {
        "type": "Info",
        "message": "Visual Dashboard başlatıldı. Ajan sistemi hazır. Görev girişi bekleniyor...",
        "time": time.strftime("%H:%M:%S")
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    # Dynamic check if ANTHROPIC_API_KEY is present
    api_status = "configured" if os.getenv("ANTHROPIC_API_KEY") else "missing_key"
    return jsonify({
        "status": "online",
        "connected_servers": ["hello_mcp", "file_system_server", "sqlite_server", "web_scraper", "memory_server"],
        "active_agent": "Autonomous Brain v2",
        "api_key_status": api_status
    })

@app.route('/api/log', methods=['POST'])
def add_log():
    data = request.json or {}
    log_type = data.get('type', 'Info')
    message = data.get('message', '')
    
    if message:
        log_item = {
            "type": log_type,
            "message": message,
            "time": time.strftime("%H:%M:%S")
        }
        logs.append(log_item)
        # Limit history size to 100 items to prevent high memory usage
        if len(logs) > 100:
            logs.pop(0)
        socketio.emit('new_log', log_item)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Mesaj boş olamaz"}), 400

def get_agent_runner():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    brain_path = os.path.join(base_dir, '06_llm_agent', 'autonomous_brain.py')
    spec = importlib.util.spec_from_file_location("autonomous_brain", brain_path)
    autonomous_brain = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(autonomous_brain)
    return autonomous_brain.run_agent_workflow

@app.route('/api/run_task', methods=['POST'])
def run_task():
    data = request.json or {}
    task_text = data.get('task')
    if not task_text:
        return jsonify({"status": "error", "message": "Görev belirtilmedi"}), 400
        
    def thread_target():
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        def callback(log_type, message):
            log_item = {
                "type": log_type,
                "message": message,
                "time": time.strftime("%H:%M:%S")
            }
            logs.append(log_item)
            if len(logs) > 100:
                logs.pop(0)
            socketio.emit('new_log', log_item)
            
        try:
            run_agent_workflow = get_agent_runner()
            # Run the agent workflow
            loop.run_until_complete(run_agent_workflow(task_text, log_callback=callback))
        except Exception as e:
            error_log = {
                "type": "Error",
                "message": f"Ajan hatası: {str(e)}",
                "time": time.strftime("%H:%M:%S")
            }
            logs.append(error_log)
            socketio.emit('new_log', error_log)
        finally:
            loop.close()
            
    threading.Thread(target=thread_target, daemon=True).start()
    return jsonify({"status": "success", "message": "Ajan görevi başlatıldı"})

@socketio.on('connect')
def handle_connect():
    print("Dashboard connected!")
    emit('server_status', {"message": "Sistem bağlantısı doğrulandı."})
    # Emitting history logs
    for log in logs:
        emit('new_log', log)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
