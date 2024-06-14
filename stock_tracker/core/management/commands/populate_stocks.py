from django.core.management.base import BaseCommand
from core.models import InvestmentAsset
import requests
import os

class Command(BaseCommand):
    help = 'Populate stocks from API'

    def handle(self, *args, **kwargs):
        API_KEY = os.getenv('API_KEY')
        if not API_KEY:
            self.stdout.write(self.style.ERROR('API_KEY is not set'))
            return

        symbols = ['RAIL3', 'ABEV3', 'BBAS3']  # Add more symbols as needed
        response = requests.get(f'https://fcsapi.com/api-v3/stock/latest?symbol={",".join(symbols)}&access_key={API_KEY}')
        
        self.stdout.write(self.style.WARNING(f'Request URL: {response.url}'))
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from API. Status code: {response.status_code}'))
            return
        
        data = response.json()
        self.stdout.write(self.style.WARNING(f'API Response: {data}'))

        if data['code'] == 200:
            unique_symbols = set()
            for item in data['response']:
                symbol = item.get('s')
                if symbol and symbol not in unique_symbols:
                    unique_symbols.add(symbol)
                    asset, created = InvestmentAsset.objects.get_or_create(
                        ticker=symbol,
                        defaults={'full_name': f'{symbol} Stock'}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created asset {symbol}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Asset {symbol} already exists'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from API. Message: {data.get("msg", "No message provided")}'))
