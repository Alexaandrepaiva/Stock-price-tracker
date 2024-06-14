import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import InvestmentAsset, PriceRecord, NotificationSetting
from .forms import InvestmentAssetForm, NotificationSettingForm
import requests
from django.utils import timezone
from datetime import timedelta

def home(request):
    asset_form = InvestmentAssetForm()
    notification_form = NotificationSettingForm()
    return render(request, 'core/home.html', {'asset_form': asset_form, 'notification_form': notification_form})

def graph(request):
    if request.method == 'POST':
        form = InvestmentAssetForm(request.POST)
        if form.is_valid():
            asset = form.cleaned_data['asset']
            quotes = PriceRecord.objects.filter(asset=asset).order_by('recorded_at')

            # Prepare data for the chart
            labels = [quote.recorded_at.strftime("%Y-%m-%d %H:%M:%S") for quote in quotes]
            prices = [float(quote.price) for quote in quotes]  # Convert Decimal to float

            context = {
                'asset': asset,
                'labels': json.dumps(labels),
                'prices': json.dumps(prices),
            }

            return render(request, 'core/graph.html', context)
    return redirect('home')

def set_notification(request):
    if request.method == 'POST':
        form = NotificationSettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return redirect('home')
