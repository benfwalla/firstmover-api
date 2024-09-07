import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate({
    "type": os.getenv("FB_TYPE"),
    "project_id": os.getenv("FB_PROJECT_ID"),
    "private_key_id": os.getenv("FB_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FB_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FB_CLIENT_EMAIL"),
    "client_id": os.getenv("FB_CLIENT_ID"),
    "auth_uri": os.getenv("FB_AUTH_URI"),
    "token_uri": os.getenv("FB_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FB_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FB_CLIENT_X509_CERT_URL")
})

firebase_admin.initialize_app(cred)

def send_push_notification_to_topic(topic, title, body, url):
    # Create the message
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={
            'url': url
        },
        topic=topic  # Send to a topic instead of a specific device token
    )

    # Send the message
    response = messaging.send(message)
    print(f"Notification sent to topic '{topic}' with response: {response}")


if __name__ == "__main__":
    topic = "test-topic"
    title = "Important Update"
    body = "There is an important update you should check out."
    url = "https://example.com/update"

    # Call the function to send the notification
    send_push_notification_to_topic(topic, title, body, url)
