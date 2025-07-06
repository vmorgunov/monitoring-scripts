import discord
from telegram import Bot
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Tokens and channel/chat IDs
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Date from which to start processing Discord messages
START_DATE = datetime(2025, 1, 1, tzinfo=timezone.utc)

# Initialize Telegram bot
telegram_bot = Bot(token=TELEGRAM_TOKEN)

# Set to keep track of processed message IDs
processed_messages = set()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if channel is None:
            print("Unable to find the specified Discord channel.")
            return

        # Load existing messages so we don't duplicate old ones
        async for message in channel.history(after=START_DATE, oldest_first=True):
            processed_messages.add(message.id)
        
        print(f'Loaded {len(processed_messages)} messages since {START_DATE.date()}.')

    async def on_message(self, message):
        # Ignore messages not in the target channel or already processed
        if message.channel.id != DISCORD_CHANNEL_ID or message.id in processed_messages:
            return

        message_time = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        telegram_message = (
            f"New message from {message.author}\n"
            f"🕒 {message_time} (UTC)\n\n"
            f"{message.content}"
        )

        await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=telegram_message)
        processed_messages.add(message.id)
        print(f"Forwarded message {message.id} to Telegram.")

# Run Discord client
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)