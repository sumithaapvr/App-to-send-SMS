from flask import Flask, render_template, jsonify
import socket
import threading
from datetime import datetime

app = Flask(__name__)

MESSAGE_FILE = 'messages.txt'

def write_message_to_file(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current time
    formatted_message = f"[{timestamp}] {message}"  # Format message with timestamp
    with open(MESSAGE_FILE, 'a') as f:  
        f.write(formatted_message + '\n')

def read_messages_from_file():
    try:
        with open(MESSAGE_FILE, 'r') as f:
            messages = f.readlines()
        return [message.strip() for message in messages] 
    except FileNotFoundError:
        return []   # Return empty if no file is found


def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Received message: {message}")
                    write_message_to_file(message)  
                    response = "SMS sent successfully!"
                    conn.sendall(response.encode())

@app.route('/')
def index():
    return render_template('server.html')

@app.route('/get_messages', methods=['GET'])
def get_messages():
    received_messages = read_messages_from_file()  
    print(f"All received messages: {received_messages}")  
    return jsonify(received_messages) 

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    app.run(port=5001, debug=True)
