import asyncio
from datetime import datetime
from dotenv import load_dotenv

import msg_config
from client import get_app
from db import engine, get_users, update_user
from models import Base, StatusChoises, User


load_dotenv()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app = get_app()
    await app.start()
    try:
        while True:
            tasks = []
            clients: list[dict[int, list[User, str]]] = []
            now = datetime.now()
            for client in await get_users():
                outgoing_text = [str(m.text).lower() async for m in app.get_chat_history(client.telegram_id)]
                cancel = any(set((word in msg_config.global_triggers for word in outgoing_text)))
                if cancel:
                    await update_user(
                        client.id,
                        status=StatusChoises.finished.value,
                        status_updated_at=now
                    )
                else:
                    clients.append({client.id: [client, outgoing_text]})
            for message_number, message in msg_config.messages.items():
                for client_id, value in clients.items():
                    if value[0].next_message_number == message_number:
                        if 'cancel_trigger' not in message or 'cancel_trigger' in message and message['cancel_trigger'] not in value[1]:
                            if now - value[0].sended_at >= message['timeout']:
                                tasks.append(app.send_message(value[0].telegram_id, message['text']))
                                await update_user(
                                    client.id,
                                    sended_at=now,
                                    next_message_number = message_number + 1
                                )
                        else:
                            await update_user(
                                    client.id,
                                    sended_at=now,
                                    next_message_number = message_number + 1
                                )
            if tasks:
                await asyncio.gather(*tasks)
            await asyncio.sleep(5)
    except asyncio.exceptions.CancelledError:
        await app.stop()


if __name__ == '__main__':
    asyncio.run(main())
