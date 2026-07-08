MAX_MESSAGE_LENGTH = 4000

def split_message(message):

    parts = []

    while len(message) > MAX_MESSAGE_LENGTH:
        parts.append(message[:MAX_MESSAGE_LENGTH])
        message = message[MAX_MESSAGE_LENGTH:]

    parts.append(message)

    return parts