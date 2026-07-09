import requests
# ضع بياناتك مباشرة هنا للتجربة فقط
TOKEN = "هنا_التوكن_الخاص_بك"
CHAT_ID = "هنا_الآي_دي_الخاص_بك"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": "اختبار مباشر من سيرفر Render"}

response = requests.post(url, data=data)
print(f"النتيجة: {response.status_code}")
print(f"الرد: {response.text}")
