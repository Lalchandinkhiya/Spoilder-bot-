import os

# Read from environment variables first, fallback to hardcoded values below.
# You can either export these in Termux:
#   export BOT_TOKEN="123456:ABC-DEF..."
#   export CHAT_ID="-1001234567890"
# or just fill them in directly here.

BOT_TOKEN = os.getenv("BOT_TOKEN", "8911725980:AAFHMKUosYGIolRnDSvwIA-M9noyPaxnXY4")

# CHAT_ID / CHANNEL_ID: the numeric ID of the channel or group to watch.
# For channels/supergroups it's usually negative, e.g. -1001234567890
CHAT_ID = int(os.getenv("CHAT_ID", os.getenv("CHANNEL_ID", "1003788523159")))
