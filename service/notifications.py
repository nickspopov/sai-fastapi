from firebase_admin import messaging


def send_push_notification_to_tokens_list(tokens: list[str], title: str, body: str) -> bool:
    if not tokens or len(tokens) == 0:
        return False
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound="default",
                ),
            ),
        ),
    )
    try:
        response = messaging.send_multicast(message)
        print(f"Successfully sent message: {response.success_count} succeeded")
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False
