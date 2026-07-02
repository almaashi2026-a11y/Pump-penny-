import requests
from bs4 import BeautifulSoup

def get_live_movers():
    """
    يقوم هذا السكربت بجلب الأسهم من Finviz بناءً على فلتر:
    - السعر: بين 0.20$ و 10$
    - الفوليوم: فوق 500k
    - الفوليوم النسبي (RVOL): أكثر من 1.5 (مؤشر انفجار)
    """
    # رابط فلتر Finviz المخصص
    url = "https://finviz.com/screener.ashx?v=111&f=sh_curvol_o500,sh_price_u10,sh_relvol_o1.5&ft=4"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # استخراج الرموز من جدول النتائج
            symbols = []
            # العناصر التي تحمل فئة 'screener-link-primary' تحتوي على رموز الأسهم
            links = soup.find_all("a", class_="screener-link-primary")
            for link in links:
                symbols.append(link.text)
            
            # إرجاع قائمة فريدة من الأسهم
            return list(set(symbols))
        else:
            print(f"فشل الاتصال بـ Finviz. كود الحالة: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"حدث خطأ أثناء جلب البيانات من Finviz: {e}")
        return []

# اختبار سريع عند تشغيل الملف بمفرده
if __name__ == "__main__":
    print("جاري البحث عن الأسهم النشطة...")
    test_symbols = get_live_movers()
    print(f"تم العثور على {len(test_symbols)} سهم: {test_symbols}")
