import asyncio
import argparse
from currency_service import CurrencyService
from websocket_chat import WebSocketChat
import websockets

async def main():
    parser = argparse.ArgumentParser(description='Отримайте курси валют ПриватБанку.')
    parser.add_argument('days', type=int, help='Кількість днів для отримання курсів (макс. 10)')
    args = parser.parse_args()

    currency_service = CurrencyService()
    rates = await currency_service.get_exchange_rates(args.days, ['EUR', 'USD'])
    
    print(rates)

if __name__ == "__main__":
    asyncio.run(main())