from flask import Flask, request, jsonify
from pyngrok import ngrok
import scrollphathd
import time
#import requests

# Initialize Flask app
app = Flask(__name__)

# Start ngrok tunnel for Flask server
def start_ngrok():
    """Start ngrok tunnel and ensure the public URL is available."""
    tunnel = ngrok.connect(5000)
    print(f"ngrok Public URL: {tunnel.public_url}")
    return tunnel.public_url

# Initialize ngrok public URL
public_url = None
for attempt in range(5):  # Retry up to 5 times to get the public URL
    try:
        public_url = start_ngrok()
        break
    except Exception as e:
        print(f"Attempt {attempt + 1}: Failed to get ngrok URL. Retrying...")
        time.sleep(2)

if not public_url:
    raise RuntimeError("Failed to start ngrok tunnel after multiple attempts.")

@app.route("/")
def home():
    return "Server is running!"

@app.route("/display", methods=["POST"])
def display_message():
    """Endpoint to display a message on the Scroll pHAT HD."""
    data = request.json
    message = data.get("message", "")

    if not message:
        return {"status": "error", "message": "No message provided"}, 400

    # Clear the Scroll pHAT HD
    scrollphathd.clear()

    # Write and scroll the message
    scrollphathd.write_string(message, brightness=0.5)
    scrollphathd.show()

    # Scroll the message
    for i in range(len(message) * 6):  # 6 pixels per character
        scrollphathd.scroll(1)
        scrollphathd.show()
        time.sleep(0.05)

    scrollphathd.clear()
    scrollphathd.show()

    return {"status": "success", "message": message}, 200

@app.route("/ngrok-url", methods=["GET"])
def get_ngrok_url():
    """Endpoint to fetch the ngrok public URL."""
    return jsonify({"url": public_url})

if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=5000)
