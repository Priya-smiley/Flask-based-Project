from flask import Flask, render_template
import numpy as np
import time
import random
import matplotlib.pyplot as plt
import io
import base64
from sklearn.metrics import classification_report, confusion_matrix

app = Flask(__name__)

# Simulated Model Performance
accuracy = 96.5
precision = 95.8
recall = 94.3
f1_score = 95.0

# Simulated Confusion Matrix
conf_matrix = np.array([[4500, 50], [60, 490]])
labels = ["Normal", "Attack"]

# Simulated Intrusion Detection Logs

attack_types = ["DDoS", "SQL Injection", "Port Scan", "Malware"]

def generate_logs():
    logs = []
    for _ in range(5):
        attack = random.choice(attack_types)
        ip = f"192.168.1.{random.randint(2, 255)}"
        timestamp = time.strftime("%H:%M:%S")
        logs.append({"time": timestamp, "type": attack, "ip": ip})
    return logs

# Function to generate attack statistics chart
def create_attack_chart():
    attack_data = {"DDoS": 120, "SQL Injection": 80, "Port Scan": 45, "Malware": 65}
    plt.figure(figsize=(5, 3))
    plt.bar(attack_data.keys(), attack_data.values(), color=['red', 'blue', 'green', 'purple'])
    plt.xlabel("Attack Type")
    plt.ylabel("Number of Attacks")
    plt.title("Detected Cyber Attacks")
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# Function to generate pie chart
def create_pie_chart():
    attack_data = {"DDoS": 120, "SQL Injection": 80, "Port Scan": 45, "Malware": 65}
    plt.figure(figsize=(5, 5))
    plt.pie(attack_data.values(), labels=attack_data.keys(), autopct='%1.1f%%', colors=['red', 'blue', 'green', 'purple'])
    plt.title("Attack Distribution")
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route('/')
def dashboard():
    logs = generate_logs()
    bar_chart = create_attack_chart()
    pie_chart = create_pie_chart()
    classification_rep = classification_report([0, 0, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0], target_names=labels)
    return render_template('dashboard.html', 
                           accuracy=accuracy, precision=precision, recall=recall, f1_score=f1_score, 
                           conf_matrix=conf_matrix, labels=labels, 
                           logs=logs, bar_chart=bar_chart, pie_chart=pie_chart, 
                           classification_rep=classification_rep)

if __name__ == '__main__':
    app.run(debug=True)
