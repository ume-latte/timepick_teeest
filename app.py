from flask import Flask, request, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# 初始化 Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return send_from_directory('static', 'TIMEPICK1.html')

@app.route('/submit-user', methods=['POST'])
def submit_user():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"error": "Name and password required"}), 400

    db.collection('users').document(name).set({
        'name': name,
        'password': password
    })
    return jsonify({"message": "User saved"})

@app.route('/submit-schedule', methods=['POST'])
def submit_schedule():
    data = request.json
    name = data.get('name')
    timetable = data.get('timetable')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    db.collection('schedules').add({
        'owner': name,
        'timetable': timetable,
        'start_time': start_time,
        'end_time': end_time,
        'start_date': start_date,
        'end_date': end_date
    })
    return jsonify({"message": "Schedule saved"})

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
