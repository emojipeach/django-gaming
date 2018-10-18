import logging

from uuid import uuid4

from django.db import models

from markets.models import Market
from markets.models import Runner

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class Bet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    market = models.ForeignKey(Market, verbose_name="Market", on_delete=models.CASCADE)
    runner = models.ForeignKey(Runner, verbose_name="Runner", on_delete=models.CASCADE)
    # owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)
    selection_name = models.CharField(max_length=50)
    odds = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)
    status = models.CharField(max_length=20, default="QUOTE")
    created_at = models.DateTimeField()

    def __str__(self):
        return self.selection_name
    
    def settle(self):
        result = self.runner.status
        if result == 'WINNER':
            self.status = result
            self.save(update_fields=['status'])
            #TODO settle account code
            return True
        elif result == 'LOSER':
            self.status = result
            self.save(update_fields=['status'])
            return True
        else:
            return False
    
    def payout_amount(self):
        return self.amount * self.odds
