# app.py
from flask import Flask, request, jsonify
from tajweed_engine import TajweedEngine

# Initialize Flask app
app = Flask(__name__)

# Load the Tajweed engine (your logic)
engine = TajweedEngine()

# --- API ENDPOINTS ---

@app.route('/feedback', methods=['POST'])
def get_feedback():
    """
    POST /feedback
    {
        "user_text": "بسم الله الرحمان الرحيم",
        "correct_text": "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ"
    }

    Returns structured Tajweed feedback.
    """
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user_text = data.get("user_text", "").strip()
    correct_text = data.get("correct_text", "").strip()

    if not user_text or not correct_text:
        return jsonify({"error": "Both 'user_text' and 'correct_text' are required"}), 400

    # Run the TajwEngine logic
    try:
        result = engine.get_feedback(user_text, correct_text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check to confirm API is live"""
    return jsonify({"status": "✅ TajwEngine API is running"}), 200


# --- RUN THE SERVER ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)