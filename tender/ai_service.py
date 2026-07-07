import anthropic
import requests
from bs4 import BeautifulSoup
from django.conf import settings


def fetch_tender_info(url: str) -> dict:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1") or soup.find("title")
        title_text = title.get_text(strip=True) if title else "Tender"

        paragraphs = soup.find_all("p")
        description = " ".join(p.get_text(strip=True) for p in paragraphs[:10])

        return {"title": title_text, "description": description[:2000]}
    except Exception:
        return {"title": "Tender", "description": ""}


def generate_tender_document(order) -> str:
    from datetime import date
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    today = date.today()
    current_date = f"{today.day}-{today.month}-{today.year}"
    current_year = today.year

    prompt = f"""Siz O'zbekistonda davlat xaridlari bo'yicha mutaxassissiz.
Quyidagi ma'lumotlar asosida rasmiy tender ariza hujjatini O'zbek tilida yozing.

BUGUNGI SANA: {current_date} ({current_year}-yil)
Hujjatda faqat {current_year}-yilni ishlat. Boshqa yil yozma.

TENDER MA'LUMOTLARI:
Tender nomi: {order.tender_title or 'Davlat xaridi'}
Tender tavsifi: {order.tender_description or 'Xarid tender'}
Tender linki: {order.tender_url}

KOMPANIYA MA'LUMOTLARI:
Kompaniya nomi: {order.company_name}
INN: {order.company_inn}
Faoliyat turi: {order.company_activity}
Tajriba: {order.company_experience}
Taklif narxi: {order.price_offer}

Quyidagi bo'limlarni o'z ichiga olgan to'liq tender arizasini yozing:

## 1. MUQADDIMA
## 2. KOMPANIYA HAQIDA
## 3. TEXNIK TAKLIF
## 4. NARX TAKLIFI
## 5. TAJRIBA VA MALAKA
## 6. XULOSA

MUHIM QOIDALAR:
- Jadvallar faqat 2-3 ustundan iborat bo'lsin, keng bo'lmasin
- Har bir jadval ustuni qisqa matn bo'lsin (30 so'zdan ko'p emas)
- Emoji ishlatma
- Kod bloki (```) ishlatma
- Hujjat rasmiy va professional uslubda yozilsin
- Markdown formatda yoz (## sarlavha, **qalin**, - ro'yxat, jadval)"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
