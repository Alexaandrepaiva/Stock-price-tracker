from django import forms
from .models import InvestmentAsset, NotificationSetting

class InvestmentAssetForm(forms.Form):
    asset = forms.ModelChoiceField(queryset=InvestmentAsset.objects.all())

class NotificationSettingForm(forms.ModelForm):
    class Meta:
        model = NotificationSetting
        fields = ['asset', 'lower_bound', 'upper_bound', 'notification_email']
