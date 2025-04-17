from flask import Flask, render_template, request
import numpy as np
import joblib  # To load trained ML model
import random
import time
import scapy.all as scapy  # For network packet analysis
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the trained AI model (assumed to be trained on NSL-KDD or CIC-IDS2017 dataset)
model = joblib.load("ids_model.pkl")  # Ensure you have a trained model saved as 'ids_model.pkl'

# Feature selection based on model training dataset
selected_features = ['duration', 'protocol_type', 'src_bytes', 'dst_bytes', 'count', 'srv_count']

# Simulated Attack Types
attack_types = ["Normal", "DDoS", "SQL Injection", "Port Scan", "Malware"]

# Function to extract network packet features
def extract_features(packet):
    try:
        duration = random.randint(1, 500)  # Simulated
        protocol_type = 1 if packet.haslayer(scapy.TCP) else (2 if packet.haslayer(scapy.UDP) else 3)
        src_bytes = len(packet.payload)
        dst_bytes = random.randint(50, 5000)  # Simulated
        count = random.randint(1, 100)
        srv_count = random.randint(1, 100)
        return np.array([duration, protocol_type, src_bytes, dst_bytes, count, srv_count]).reshape(1, -1)
    except:
        return None

# Function to capture and classify packets
def capture_packets():
    logs = []
    for _ in range(5):
        packet = scapy.IP()/scapy.TCP()  # Simulated packet
        features = extract_features(packet)
        if features is not None:
            prediction = model.predict(features)[0]
            attack = attack_types[prediction]
            ip = f"192.168.1.{random.randint(2, 255)}"
            timestamp = time.strftime("%H:%M:%S")
            logs.append({"time": timestamp, "type": attack, "ip": ip})
    return logs

# Function to generate attack statistics chart
def create_attack_chart():
    attack_data = {"DDoS": 120, "SQL Injection": 80, "Port Scan": 45, "Malware": 65, "Normal": 300}
    plt.figure(figsize=(5, 3))
    plt.bar(attack_data.keys(), attack_data.values(), color=['red', 'blue', 'green', 'purple', 'gray'])
    plt.xlabel("Attack Type")
    plt.ylabel("Number of Attacks")
    plt.title("Detected Cyber Attacks")
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/')
def dashboard():
    logs = capture_packets()
    attack_chart = create_attack_chart()
    return render_template('dashboard.html', logs=logs, attack_chart=attack_chart)

if __name__ == '__main__':
    app.run(debug=True)
