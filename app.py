# app.py
from flask import Flask, request, jsonify
from tajweed_engine import TajweedEngine
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Allow JSON decoding of incoming requests
app.config['JSON_AS_ASCII'] = False

# Initialize the Tajweed engine
try:
    engine = TajweedEngine()
    logger.info("TajweedEngine initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize TajweedEngine: {e}")
    engine = None

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
    if not request.is_json:
        logger.warning("Received non-JSON request")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    logger.info(f"Received data: {data}")

    # Validate input
    user_text = data.get("user_text", "").strip()
    correct_text = data.get("correct_text", "").strip()

    if not user_text or not correct_text:
        logger.warning("Missing user_text or correct_text in request")
        return jsonify({"error": "Both 'user_text' and 'correct_text' are required"}), 400

    if engine is None:
        logger.error("TajweedEngine not initialized")
        return jsonify({"error": "Internal server error: Engine not available"}), 500

    # Run the TajwEngine logic
    try:
        result = engine.get_feedback(user_text, correct_text)
        logger.info("Feedback generated successfully")
        return jsonify(result), 200
    except Exception as e:
        logger.exception(f"Error in TajweedEngine.get_feedback: {e}")
        return jsonify({"error": f"Internal error during processing: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check to confirm API is live"""
    logger.info("Health check requested")
    return jsonify({"status": "✅ TajwEngine API is running"}), 200

# --- RUN THE SERVER ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)