import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("siskam-df66d-firebase-adminsdk-q6lbj-561ad6009d.json")
firebase_admin.initialize_app(cred)

def pushNotif(tokens_list):
    message = messaging.MulticastMessage(
        tokens=tokens_list,
        notification=messaging.Notification(
            title="Peringatan!",
            body="Gerakan Terdeteksi"
        ),
    )
    response = messaging.send_multicast(message)
    print(f"Successfully sent {response.success_count} messages")
    print(f"Failed to send {response.failure_count} messages")

