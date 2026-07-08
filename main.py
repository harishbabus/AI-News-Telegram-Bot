from telegram_bot import send_message

message = """
🤖 AI News Bot

Hello Harish!

Project structure is now modular.
"""

if send_message(message):
    print("Message sent!")
else:
    print("Failed.")