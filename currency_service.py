import aiohttp
import asyncio
from datetime import datetime, timedelta

class CurrencyService:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def get_exchange_rates(self, days: int, currencies: list):
        if days < 1 or days > 10:
            raise ValueError("Кількість днів має бути від 1 до 10.")

        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_rates(session, (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y'), currencies) for i in range(days)]
            return await asyncio.gather(*tasks)

    async def _fetch_rates(self, session, date, currencies):
        async with session.get(f"{self.API_URL}?date={date}") as response:
            if response.status != 200:
                raise Exception(f"Не вдалося отримати дані: {response.status}")

            data = await response.json()

            result = {data['date']: {}}

            for rate in data['exchangeRate']:
                if rate['currency'] in currencies:
                    result[data['date']][rate['currency']] = {
                        'sale': rate.get('saleRate', rate.get('saleRateNB')),
                        'purchase': rate.get('purchaseRate', rate.get('purchaseRateNB'))
                    }

            return result