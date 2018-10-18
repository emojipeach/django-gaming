import datetime
import logging
import pytz

from uuid import uuid4

from django.db import models

from api_viewer.utils import list_market_book

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class Market(models.Model):
    """ Market data."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    market_id = models.FloatField(unique=True)
    event_id = models.IntegerField()
    country = models.CharField(max_length=10)
    sport = models.CharField(max_length=50)
    competition_name = models.CharField(max_length=50)
    event_name = models.CharField(max_length=50)
    market_name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    timezone = models.CharField(max_length=50)
    number_runners = models.IntegerField()
    total_matched = models.IntegerField(blank=True)
    last_updated = models.DateTimeField()
    suspended = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    
    def __str__(self):
        return '{0} {1}'.format(self.event_name, self.market_name)
    
    def update(self):
        market_book = list_market_book(self.market_id)
        runners = Runner.objects.filter(market=self.id).order_by('sort_priority')
        count = 0
        for runner in runners:
            runner.latest_odds = market_book['runners'][count]['lastPriceTraded']
            runner.save()
            count += 1
        self.last_updated = datetime.datetime.now(pytz.timezone('UTC'))
        return True

    def settle(self):
        market_book = list_market_book(self.market_id)
        try:
            market_book['runners'][0]['status']
            runners = Runner.objects.filter(market=self.id).order_by('sort_priority')
            for runner in runners:
                count = 0
                while runner.selection_id != market_book['runners'][count]['selectionId']:
                    count += 1
                runner.status = market_book['runners'][count]['status']
                runner.save(update_fields=['status'])
        except KeyError:
            return False
        self.settled = True
        self.save(update_fields=['settled'])
        return True


class Runner(models.Model):
    """ Runner data."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    selection_id = models.IntegerField()
    selection_name = models.CharField(max_length=50)
    sort_priority = models.IntegerField()
    latest_odds = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, default="ACTIVE")
    
    def __str__(self):
        return self.selection_name

