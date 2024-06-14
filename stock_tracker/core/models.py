from django.db import models

class InvestmentAsset(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    min_price_threshold = models.FloatField(null=True, blank=True)
    max_price_threshold = models.FloatField(null=True, blank=True)
    tracking_interval = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def toggle_tracking_status(self):
        self.is_active = not self.is_active

    def update_thresholds(self, new_min_price, new_max_price, new_tracking_interval):
        self.min_price_threshold = new_min_price
        self.max_price_threshold = new_max_price
        self.tracking_interval = new_tracking_interval

    def __str__(self):
        return self.full_name

class PriceRecord(models.Model):
    asset = models.ForeignKey(InvestmentAsset, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    suggested_action = models.CharField(max_length=10, null=True, blank=True)

class NotificationSetting(models.Model):
    asset = models.ForeignKey(InvestmentAsset, on_delete=models.CASCADE)
    lower_bound = models.DecimalField(max_digits=10, decimal_places=2)
    upper_bound = models.DecimalField(max_digits=10, decimal_places=2)
    notification_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
