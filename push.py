import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate('firebase-admin.json')
firebase_admin.initialize_app(cred)


def send_push_notification(fcm_token, title, body):
    # Define the message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token,
    )

    # Send the message
    try:
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")


if __name__ == "__main__":
    ben_fcm_token = os.getenv("ben_fcm_token")
    send_push_notification(ben_fcm_token, "Hello!", "This is a push notification.")
