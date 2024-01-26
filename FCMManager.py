from firebase_admin import credentials, messaging


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

