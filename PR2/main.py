# main.py

import threading
import time
from chat_room import app, socketio
from server import run_http_server

def start_http_server():
    run_http_server()

def start_flask_socketio_server():
    socketio.run(app, port=5000)

if __name__ == "__main__":
    # Create threads for both servers
    http_thread = threading.Thread(target=start_http_server)
    flask_thread = threading.Thread(target=start_flask_socketio_server)

    # Start both threads
    http_thread.start()
    flask_thread.start()

    # Optionally, wait for both threads to finish
    http_thread.join()
    flask_thread.join()
