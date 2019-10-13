from django.db import models
from datetime import datetime, timedelta, date
from calendar import monthrange

from budget.frequency.models import Frequency
from budget.client.models import Client


class Income(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    last_paid = models.DateField(null=True)
    last_modified = models.DateField(auto_now=True)

    def next_paid(self, _date=None):
        if self.title == 'monthly':
            delta = timedelta(
                monthrange(
                    self.last_paid.year, self.last_paid.month)[1]
                    )
        else:
            delta = timedelta(days=365 // self.frequency.number_of_paychecks)
        if _date == None:
            next_due = self.last_paid + delta
        else:
            next_due = _date + delta

        return next_due

    def get_attributes(self):
        return [
            'title',
            'amount',
            'frequency',
            'last_paid'
        ]

    def __str__(self):
        return self.title
