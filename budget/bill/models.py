from django.db import models
from datetime import datetime, timedelta, date
from calendar import monthrange

from budget.client.models import Client
from budget.frequency.models import Frequency


class Bill(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    last_paid = models.DateField(null=True)
    weekdays_only = models.BooleanField(default=True)

    last_modified = models.DateField(auto_now=True, editable=True)

    def days_between(self):
        if self.frequency.title == 'monthly':
            delta = timedelta(
                monthrange(
                    self.last_paid.year, self.last_paid.month)[1]
            )
        else:
            delta = timedelta(days=365 // self.frequency.number_of_paychecks)

        return delta.days

    def next_due(self, _date=None):
        if _date == None:
            next_due = self.last_paid + timedelta(days=self.days_between())
        else:
            next_due = _date + timedelta(days=self.days_between())

        while next_due.weekday() > 5:
            next_due -= timedelta(days=1)

        return next_due

    def get_attributes(self):
        return [
            'title',
            'amount',
            'frequency',
            'last_paid',
            'weekdays_only'
        ]

    def __str__(self):
        return self.title
