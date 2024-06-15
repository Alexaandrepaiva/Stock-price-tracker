import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import InvestmentAsset, PriceRecord, NotificationSetting
from .forms import InvestmentAssetForm, NotificationSettingForm
from .tasks import create_schedule_task
from django.contrib import messages
import requests

def home(request):
    asset_form = InvestmentAssetForm()
    notification_form = NotificationSettingForm()
    return render(request, 'core/home.html', {'asset_form': asset_form, 'notification_form': notification_form})

def graph(request):
    if request.method == 'POST':
        form = InvestmentAssetForm(request.POST)
        if form.is_valid():
            asset = form.cleaned_data['asset']
            quotes = PriceRecord.objects.filter(asset=asset).order_by('-recorded_at')[:20]  # Get the latest 20 records

            # Reverse the order to show the oldest first
            quotes = quotes[::-1]

            labels = [quote.recorded_at.strftime("%Y-%m-%d %H:%M:%S") for quote in quotes]
            prices = [float(quote.price) for quote in quotes]

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
            notification = form.save()
            create_schedule_task.delay(
                notification.asset.id,
                notification.lower_bound,
                notification.upper_bound,
                notification.notification_email,
                notification.interval_minutes
            )
            messages.success(request, 'Email notification successfully set!')
        else:
            messages.error(request, 'Failed to set email notification. Please check the form and try again.')
        return redirect('home')
    return redirect('home')