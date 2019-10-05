from django.db import models

from budget.client.models import Client


class Bill(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    day_due = models.IntegerField()
    weekdays_only = models.BooleanField(default=True)

    last_modified = models.DateField(auto_now=True, editable=True)
