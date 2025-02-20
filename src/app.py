import logging
import json
import datetime
import os

import requests
from flask import Flask, request

app = Flask(__name__)
app.logger.setLevel(logging.INFO)  # Ensure INFO logs appear in container logs

PUSHBULLET_ACCESS_TOKEN = os.environ.get("PUSHBULLET_ACCESS_TOKEN")
GOTIFY_ACCESS_TOKEN = os.environ.get("GOTIFY_ACCESS_TOKEN")
GOTIFY_SERVER_URL = os.environ.get("GOTIFY_SERVER_URL")

@app.route("/forward", methods=["POST"])
def forward():
    
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No valid JSON received.")
        
        app.logger.info("Notification received.")

        # extract notification data
        display_name = data["Notifications"][0]["App"]["DisplayName"]
        title = data["Notifications"][0]["Title"]
        content = data["Notifications"][0]["Content"]
        new_title = f"[{display_name}] {title}"

        destination = request.args.get("dest", "gotify").lower()  # default destination to "gotify"

        if destination == "pb":
            # destination=pushbullet
            if not PUSHBULLET_ACCESS_TOKEN:
                raise ValueError("Missing PUSHBULLET_ACCESS_TOKEN env var for 'pb' destination.")

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
                    f"Failed to forward notification to Pushbullet. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )

        else:
            # destination=gotify (default)
            if not GOTIFY_ACCESS_TOKEN:
                raise ValueError("Missing GOTIFY_ACCESS_TOKEN env var for 'gotify' destination.")
            
            # get priority (default to 5)
            priority_param = request.args.get("p", "5")
            try:
                priority = int(priority_param)
                if not (0 <= priority <= 10):
                    raise ValueError
            except ValueError:
                app.logger.error(f"Invalid priority value: {priority_param}")
                return abort(400, "Priority must be an integer between 0 and 10.")

            # send to gotify
            response = requests.post(
                f"{GOTIFY_SERVER_URL}/message?token={GOTIFY_ACCESS_TOKEN}",
                files={
                    "title": (None, new_title),
                    "message": (None, content),
                    "priority": (None, str(priority))
                }
            )

            if response.status_code == 200:
                app.logger.info("Notification successfully forwarded to Gotify.")
            else:
                app.logger.error(
                    f"Failed to forward notification to Gotify. "
                    f"Status: {response.status_code}, Response: {response.text}"
                )

        # Log the entire notification to file for record-keeping
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
    app.run(host="0.0.0.0", port=80)
