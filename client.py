import os
from pyrogram import Client, filters

from db import add_user


def get_app():

    app = Client(os.getenv('ACCOUNT_NAME'), api_id=os.getenv('API_ID'), api_hash=os.getenv('API_HASH'))

    @app.on_message(filters.private & filters.text & ~filters.me)
    async def save(client, message):
        await add_user(message.chat.username, message.chat.id)
    return app
