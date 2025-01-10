# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from bias_detect import BiasDetector

app = Flask(__name__)
CORS(app)  # This allows your React frontend to call this API

detector = BiasDetector()

@app.route('/')
def home():
    return "Flask backend is running!"

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    if not text.strip():
        return jsonify({"error": "Empty text provided"}), 400
    
    result = detector.analyze_text(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)