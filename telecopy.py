"""
Make full copy of telegram channel
"""
import time
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.types import MessageService,InputMessagesFilterPhotoVideo
from decouple import config

# put your values
# Telegram API
API_ID = config("APP_ID", default=0, cast=int)
API_HASH = config("API_HASH", default=None, cast=str)
SESSION_STRING = config("SESSION", default="", cast=str)
SOURCE_CHAT = config("FROM_CHANNEL", default="", cast=str)
TARGET_CHAT = config("TO_CHANNEL", default="", cast=str)
# Timeout after 50 messages
LIMIT_TO_WAIT = 50


def do_full_copy():
    with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        amount_sended = 0
        for message in client.iter_messages(int(SOURCE_CHAT), filter=InputMessagesFilterPhotoVideo, reverse=True):
            # skip if service messages
            if isinstance(message, MessageService):
                continue
            try:
                print(f'Raw Message : {message.message}')
                message.message = message.message + f'\nMessage ID: {message.id}'
                client.send_message(int(TARGET_CHAT), message)
                print(f'Sended Message to: {TARGET_CHAT}\nMessage ID: {message.id}')
                amount_sended += 1
                if amount_sended >= LIMIT_TO_WAIT:
                    amount_sended = 0
                    time.sleep(1)
            except Exception as e:
                print(e)

        print("Done")


if __name__ == "__main__":
    do_full_copy()