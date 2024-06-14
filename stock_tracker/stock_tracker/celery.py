from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_tracker.settings')

app = Celery('stock_tracker')
app.conf.enable_utc = False
app.conf.update(timezone='America/Sao_Paulo')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'fetch-asset-prices-every-2-minutes': {
        'task': 'core.tasks.fetch_asset_prices',
        'schedule': crontab(minute='*/2'),  # every 2 minutes
    },
}
