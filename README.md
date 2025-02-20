# Notification Forwarder Adapter
This is a lightweight web service that works as a Pushbullet or Gotify adapter for the Notification Forwarder Windows app ([Elepover/notificationforwarder](https://github.com/Elepover/notificationforwarder)). It does the following:

1. Receives notifications from Notification Forwarder
1. Parses the notification and repackages it
1. Forwards it again to either Pushbullet or Gotify.

## Notification Forwarder Format
Notifications received from the Notification Forwarder application will have the following format:

```json
{
    "ClientVersion": "1.4.29.0",
    "Notifications": [
        {
            "App": {
                "AppUserModelId": "Microsoft.MicrosoftEdge.Stable_xxxxxx!App",
                "Id": "App",
                "DisplayName": "Microsoft Edge",
                "ForwardingEnabled": true
            },
            "TimeStamp": "2025-01-29T12:32:50.7264485",
            "Title": "Test Notification", 
            "Content": "Testing 1, 2, 3!"
        }
    ]
}
```
