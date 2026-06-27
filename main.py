#!/usr/bin/env python3
"""
Minimal Telegram bot (aiogram 3.x) that auto-marks every video
posted in a specific channel/group as "Spoiler".

Flow:
  1. Video arrives in the watched chat.
  2. Bot re-sends it using the same file_id with has_spoiler=True.
  3. Bot deletes the original (non-spoiler) message.

No DB, no admin panel, no extra logging beyond basic console prints.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, CHAT_ID

# Basic console logging only
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("spoiler_bot")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher()


async def handle_video(message: Message) -> None:
    """Re-send the video with spoiler enabled, then delete the original."""
    # Skip if it's already a spoiler (avoid re-processing our own resend)
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
        log.info(f"Spoiler applied to video in chat {message.chat.id} (msg {message.message_id})")
    except TelegramBadRequest as e:
        log.info(f"Could not process video {message.message_id}: {e}")


# Regular groups / private chats use "message" updates
@dp.message(F.chat.id == CHAT_ID, F.video)
async def on_message_video(message: Message) -> None:
    await handle_video(message)


# Channels deliver posts as "channel_post" updates
@dp.channel_post(F.chat.id == CHAT_ID, F.video)
async def on_channel_post_video(message: Message) -> None:
    await handle_video(message)


async def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
        raise SystemExit("BOT_TOKEN is not set. Set it via env var or config.py")
    if not CHAT_ID:
        raise SystemExit("CHAT_ID is not set. Set it via env var or config.py")

    log.info("Bot starting... watching chat_id=%s", CHAT_ID)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "channel_post"])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped.")
