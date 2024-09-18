import asyncio
import websockets
import json
from aiofile import AIOFile, Writer
from aiopath import Path
from currency_service import CurrencyService

class WebSocketChat:
    def __init__(self, currency_service):
        self.currency_service = currency_service

    async def start_chat(self, websocket, path):
        async for message in websocket:
            await self.handle_message(websocket, message)

    async def handle_message(self, websocket, message):
        command = message.split()
        
        if command[0] == "exchange":
            days = int(command[1]) if len(command) > 1 else 1
            await self.send_exchange_rates(websocket, days)
        else:
            await websocket.send("Невідома команда")

    async def send_exchange_rates(self, websocket, days):
        currencies = ['EUR', 'USD']
        rates = await self.currency_service.get_exchange_rates(days, currencies)
        await websocket.send(json.dumps(rates))
        
        await self.log_exchange_command(days)

    async def log_exchange_command(self, days):
        async with AIOFile('exchange_log.txt', 'a') as afp:
            writer = Writer(afp)
            await writer(f"Команда exchange виконана: {days} днів\n")