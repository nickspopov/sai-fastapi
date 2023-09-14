
from typing import List
from firebase_admin import messaging

def send_push_notification_to_tokens_list(tokens: List[str], title: str, body: str) -> bool:
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
                    sound='default',
                ),
            ),
        ),
    )
    try: 
      response = messaging.send_multicast(message)
      print('Successfully sent message:', response)
      return True
    except:
      print('Error sending message')
      return False