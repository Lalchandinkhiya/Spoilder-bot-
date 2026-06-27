# Spoiler Bot

A tiny Telegram bot (aiogram 3.x) that automatically marks every video posted
in a specific channel or group as **"Spoiler"**.

No database, no admin panel, no extras — just watches one chat, re-sends
videos with the spoiler effect enabled, and deletes the original.

## How it works

1. Bot watches one chat (channel or group) by `chat_id`.
2. When a video appears, the bot re-sends it (same file, same caption) with
   `has_spoiler=True`.
3. The original (non-spoiler) message is deleted.

## Requirements

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- The bot must be an **admin** in the target channel/group, with permission
  to post messages and delete messages.

## Setup (Termux)

```bash
pkg install python -y
pip install -r requirements.txt
```

### Configure

Set your bot token and target chat ID, either as environment variables:

```bash
export BOT_TOKEN="123456:ABC-DEF..."
export CHAT_ID="-1001234567890"
```

...or by editing `config.py` directly and filling in the placeholder values.

**Getting the chat ID:** add the bot to your channel/group as admin, post any
message, and check it via `https://api.telegram.org/bot<token>/getUpdates`,
or use a helper bot like @getidsbot.

## Run

```bash
python main.py
```

Keep it running in the background on Termux with:

```bash
nohup python main.py > bot.log 2>&1 &
```

or run it inside a `tmux`/`screen` session so it survives terminal closure.

## Notes

- Designed to be minimal: low RAM/CPU usage, no persistent storage.
- Only videos are processed; all other content is ignored.
- If the bot lacks delete permission, the spoiler copy will still be sent,
  but the original message will remain.
