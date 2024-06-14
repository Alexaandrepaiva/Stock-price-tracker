import os
import requests
import smtplib
import json
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.mail import send_mail
from django.conf import settings
from .models import InvestmentAsset, PriceRecord, NotificationSetting

# Load environment variables
API_KEY = os.getenv('API_KEY')
SENDER_MAIL = os.getenv('SENDER_MAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

@shared_task
def fetch_asset_prices():
    assets = InvestmentAsset.objects.all()
    symbols = ','.join([asset.ticker for asset in assets])
    response = requests.get(f'https://fcsapi.com/api-v3/stock/latest?symbol={symbols}&access_key={API_KEY}')
    data = response.json()
    if data['code'] == 200:
        for item in data['response']:
            symbol = item.get('s')
            if symbol:
                asset = InvestmentAsset.objects.get(ticker=symbol)
                price = float(item['c'])
                PriceRecord.objects.create(asset=asset, price=price)
                evaluate_price_thresholds(asset, price)

def evaluate_price_thresholds(asset, price):
    settings = NotificationSetting.objects.filter(asset=asset)
    for setting in settings:
        if price < setting.lower_bound or price > setting.upper_bound:
            action = "Buy" if price < setting.lower_bound else "Sell"
            send_alert(setting.notification_email, asset.full_name, price, action)
            PriceRecord.objects.create(asset=asset, price=price, suggested_action=action)

def send_alert(email, asset_name, price, action):
    subject = f'Stock Alert for {asset_name}'
    message = f'The price of {asset_name} is now {price}. Recommended action: {action}.'
    send_mail(subject, message, SENDER_MAIL, [email], fail_silently=False)


@shared_task
def create_schedule_task(asset_id, lower_bound, upper_bound, email, interval_minutes):
    asset = InvestmentAsset.objects.get(id=asset_id)
    schedule, created = IntervalSchedule.objects.get_or_create(every=interval_minutes, period=IntervalSchedule.MINUTES)
    PeriodicTask.objects.create(
        name=f"{asset.ticker}_task",
        task="core.tasks.fetch_asset_prices",
        interval=schedule,
    )
    NotificationSetting.objects.create(asset=asset, lower_bound=lower_bound, upper_bound=upper_bound, notification_email=email)
    return "Scheduled Task and Notification Setting created"
