from django.contrib import admin
from .models import InvestmentAsset, PriceRecord, NotificationSetting

admin.site.register(InvestmentAsset)
admin.site.register(PriceRecord)
admin.site.register(NotificationSetting)
