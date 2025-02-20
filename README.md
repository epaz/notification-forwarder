# Notification Forwarder Adaptor
This is a lightweight web service that works as a Pushbullet or Gotify adaptor for the Notification Forwarder Windows app ([Elepover/notificationforwarder](https://github.com/Elepover/notificationforwarder)). It does the following:

1. Receives notifications from Notification Forwarder
1. Parses the notification and repackages it
1. Forwards it again to either Pushbullet or Gotify.

## API

### Forward Notification
`POST /forward?dest=[destination]&p=[priority]`
- Forwards a notification
- `dest` - query param to determine forward destination
   - `pb` for Pushbullet
   - `gotify` for Gotify
   - _Defaults to `gotify`_
- `p` - priority. **Only used when forwarding to Gotify**
   - Must be an integer from `0` to `10`
   - _Defaults to `5`_

## Configuration

- `PUSHBULLET_ACCESS_TOKEN` - Pushbullet API Access Token
- `GOTIFY_SERVER_URL` - Full URL of the Gotify server you wish to use
- `GOTIFY_ACCESS_TOKEN` - Gotify Access Token (requires creating an "App" within Gotify)

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
