import requests
from bs4 import BeautifulSoup

def get_live_movers():
    # هذا الرابط يحتوي على الفلتر: السعر من 0.2$ إلى 10$ + فوليوم فوق 500k + فوليوم نسبي فوق 1.5
    url = "https://finviz.com/screener.ashx?v=111&f=sh_curvol_o500,sh_price_u10,sh_relvol_o1.5&ft=4"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # استخراج الرموز من الجدول
            symbols = [link.text for link in soup.find_all("a", class_="screener-link-primary")]
            return list(set(symbols)) # إرجاع القائمة بدون تكرار
        return []
    except Exception as e:
        print(f"Error fetching Finviz: {e}")
        return []
