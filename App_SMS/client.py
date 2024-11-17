from flask import Flask, render_template, request, jsonify
import socket
import json

app = Flask(__name__)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def send_sms(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        return response

@app.route('/')
def index():
    return render_template('client.html')

@app.route('/send_sms', methods=['POST'])
def send_sms_route():
    message = request.form.get('message')
    if message:
        response = send_sms(message)
        return jsonify({'status': 'success', 'response': response})
    return jsonify({'status': 'error', 'response': 'No message provided.'})

if __name__ == '__main__':
    app.run(port=5000, debug=True) 