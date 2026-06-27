#!/usr/bin/env python3
"""
Minimal Telegram bot (aiogram 3.x) that auto-marks every video
posted in a specific channel/group as "Spoiler".
"""

import asyncio
import logging
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, CHAT_ID

# ------------------ Render Web Server ------------------

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Spoiler Bot is Running!")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# ------------------ Logging ------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("spoiler_bot")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher()

# ------------------ Bot Logic ------------------

async def handle_video(message: Message):
    if message.has_media_spoiler:
        return

    try:
        await bot.send_video(
            chat_id=message.chat.id,
            video=message.video.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            has_spoiler=True,
        )
        await message.delete()
        log.info(f"Spoiler applied: {message.message_id}")
    except TelegramBadRequest as e:
        log.info(e)


@dp.message(F.chat.id == CHAT_ID, F.video)
async def on_message_video(message: Message):
    await handle_video(message)


@dp.channel_post(F.chat.id == CHAT_ID, F.video)
async def on_channel_post_video(message: Message):
    await handle_video(message)

# ------------------ Main ------------------

async def main():
    Thread(target=run_web, daemon=True).start()

    log.info("Bot starting... watching chat_id=%s", CHAT_ID)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=["message", "channel_post"]
    )


if __name__ == "__main__":
    asyncio.run(main())
