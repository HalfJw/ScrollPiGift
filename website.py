from flask import Flask, request, jsonify
from pyngrok import ngrok
import scrollphathd
import time

# Initialize Flask app
app = Flask(__name__)

# Start ngrok tunnel for Flask server
public_url = ngrok.connect(5000)
print(f"ngrok Public URL: {public_url}")

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
