import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(symbol, strength, money_flow, targets):
    message = (
        f"🚀 **فرصة انفجار محتملة!**\n\n"
        f"📈 **السهم:** ${symbol}\n"
        f"🔥 **قوة الزخم (Score):** {strength}/10\n"
        f"💰 **تدفق السيولة:** {money_flow}\n"
        f"🎯 **الأهداف المتوقعة:** {targets[0]} | {targets[1]}\n\n"
        f"🔗 [شاهد السهم على Finviz](https://finviz.com/quote.ashx?t={symbol})"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    requests.post(url, params=params)
