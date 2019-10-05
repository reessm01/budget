from django.db import models

from budget.frequency.models import Frequency
from budget.client.models import Client


class Income(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    init_paid = models.DateField()

    last_modified = models.DateField(auto_now=True)
