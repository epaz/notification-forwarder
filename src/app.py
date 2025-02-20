import logging
import json
import datetime
import os

import requests
from flask import Flask, request

app = Flask(__name__)
app.logger.setLevel(logging.INFO)  # Ensure INFO logs appear in container logs

PUSHBULLET_ACCESS_TOKEN = os.environ.get("PUSHBULLET_ACCESS_TOKEN")
if not PUSHBULLET_ACCESS_TOKEN:
    raise ValueError("Missing environment variable: PUSHBULLET_ACCESS_TOKEN")

@app.route("/notify", methods=["POST"])
def notify():
    """Receives JSON data, forwards the title and content to Pushbullet, logs result."""
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No valid JSON received.")

        # Log the fact a notification was received
        app.logger.info("Notification received.")

        # Extract the relevant fields
        # The structure you showed is data["Notifications"][0]["App"]["DisplayName"], etc.
        display_name = data["Notifications"][0]["App"]["DisplayName"]
        title = data["Notifications"][0]["Title"]
        content = data["Notifications"][0]["Content"]

        # Create the new title
        new_title = f"[{display_name}] {title}"

        # Send to Pushbullet
        push_data = {
            "type": "note",
            "title": new_title,
            "body": content
        }
        headers = {
            "Access-Token": PUSHBULLET_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }
        response = requests.post("https://api.pushbullet.com/v2/pushes", 
                                 headers=headers, json=push_data)

        if response.status_code == 200:
            app.logger.info("Notification successfully forwarded to Pushbullet.")
        else:
            app.logger.error(
                f"Failed to forward notification. "
                f"Status: {response.status_code}, Response: {response.text}"
            )

        # Log the entire notification to file for record-keeping
        # Adjust path if mounting a different directory
        with open("/app/data/api.log", "a") as log_file:
            log_file.write(json.dumps(data) + "\n")

        return "Notification processed.\n", 200

    except Exception as e:
        app.logger.error(f"Error handling notification: {str(e)}")
        return "Error processing notification.\n", 400

@app.route("/health", methods=["GET"])
def health_check():
    current_time = datetime.datetime.utcnow().isoformat()
    return f"Service is running! Timestamp: {current_time}\n", 200

if __name__ == "__main__":
    # Listen on port 80 for your reverse proxy setup
    app.run(host="0.0.0.0", port=80)
