Baleh
An advanced Python library for Bale messenger bots, inspired by Telegram Bot API.

Installation
bash

کپی
pip install baleh
Features
Send text messages, photos, videos, audio, stickers, and documents
Manage chats (get chat info, ban/unban members)
Handle incoming messages with decorators
Asynchronous API with aiohttp
Webhook support
Type hints for better IDE support
Usage
Send a Message
python

کپی
from baleh import BaleClient
import asyncio

async def main():
    client = BaleClient("your_bot_token")
    await client.connect()
    message = await client.send_message(chat_id=123456789, text="Hello, Bale!")
    print(message.text)
    await client.disconnect()

asyncio.run(main())
Send a Photo
python

کپی
async def send_photo():
    client = BaleClient("your_bot_token")
    await client.connect()
    message = await client.send_photo(chat_id=123456789, photo="path/to/photo.jpg", caption="My photo")
    await client.disconnect()

asyncio.run(send_photo())
Handle Incoming Messages
python

کپی
async def handle_messages():
    client = BaleClient("your_bot_token")
    
    @client.on_message()
    async def on_message(message):
        await client.send_message(message.chat.id, f"Received: {message.text}")
    
    await client.connect()
    await client.start_polling()

asyncio.run(handle_messages())
Contributing
Fork the repository at github.com/hamidrashidi98/baleh and submit pull requests.