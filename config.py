import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))
INTERVAL = int(os.getenv('INTERVAL'))
TIMEZONE = os.getenv('TIMEZONE')

PRICE_TEXT = """💲 *Tether Price*
🗓 *{date}*
⏰ *{time}*
{prices}
"""
PRICE_FORMAT = """
🌐 *{source}*
🔹 *Buy:* `{buy}`
🔸 *Sell:* `{sell}`
 """
