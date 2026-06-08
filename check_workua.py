import asyncio
import httpx
from bs4 import BeautifulSoup

async def check():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    async with httpx.AsyncClient(headers=headers) as client:
        r = await client.get("https://www.work.ua/jobs-python/")
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.select("div.card.card-hover.job-link")
        
        # виводимо HTML першої вакансії
        print(items[0].prettify()[:5000])

asyncio.run(check())