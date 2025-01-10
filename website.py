from flask import Flask, request
import scrollphathd
import time

app = Flask(__name__)

@app.route('/display', methods=['POST'])
def display_message():
    # Get the message from the POST request
    data = request.json
    message = data.get('message', '')

    if not message:
        return {"status": "error", "message": "No message provided"}, 400

    # Clear the Scroll pHAT HD
    scrollphathd.clear()

    # Display the message
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
