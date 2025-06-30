import os
import logging
import datetime
import asyncio
from telegram import Bot
from tvDatafeed import TvDatafeed, Interval
from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
TV_USER = os.getenv("TV_USER")
TV_PASSWORD = os.getenv("TV_PASSWORD")

bot = Bot(token=TELEGRAM_TOKEN)
tv = TvDatafeed(username=TV_USER, password=TV_PASSWORD)

symbols = [
    'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD',
    'USDCHF', 'NZDUSD', 'EURJPY', 'EURGBP', 'GBPJPY',
    'CHFJPY', 'AUDJPY', 'EURNZD', 'GBPCHF', 'NZDJPY'
]

async def monitor_rsi():
    while True:
        now = datetime.datetime.utcnow()
        if now.minute % 5 == 4 and now.second == 0:
            for symbol in symbols:
                try:
                    data = tv.get_hist(symbol=symbol, exchange='FXCM', interval=Interval.in_5_minute, n_bars=2)
                    last_rsi = data['rsi'].iloc[-1]
                    if last_rsi < 20 or last_rsi > 70:
                        condition = "🟢 RSI > 70 (Ipercomprato)" if last_rsi > 70 else "🔴 RSI < 20 (Ipervenduto)"
                        await bot.send_message(chat_id=TELEGRAM_USER_ID, text=f"⚠️ {condition} su {symbol}\nRSI: {last_rsi:.2f}")
                except Exception as e:
                    logging.error(f"Errore su {symbol}: {e}")
            await asyncio.sleep(60)
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(monitor_rsi())