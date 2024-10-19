import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate('firebase-admin.json')
firebase_admin.initialize_app(cred)


def send_push_notification(fcm_tokens, title, body):
    """
    Send a push notification to multiple FCM tokens.

    Args:
        fcm_tokens (List[str]): A list of FCM registration tokens.
        title (str): The title of the notification.
        body (str): The body of the notification.

    Returns:
        response (messaging.BatchResponse): A response object containing the results of the send
            operation.

    Raises:
        Exception: If an error occurs while sending the message.
    """
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=fcm_tokens,
    )

    try:
        response = messaging.send_each_for_multicast(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")


if __name__ == "__main__":
    ben_fcm_token = os.getenv("ben_fcm_token")
    send_push_notification([ben_fcm_token], "Hello!", "This is a push notification.")
