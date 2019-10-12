from django.db import models

from budget.client.models import Client


class CheckIn(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(editable=True)
    projected_balance = models.DecimalField(max_digits=12, decimal_places=2)
    futures_balance = models.DecimalField(max_digits=12, decimal_places=2)
    outgoing_balance = models.DecimalField(max_digits=12, decimal_places=2)
    actual_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
        )
    difference = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
        )

    last_modified = models.DateField(auto_now=True, editable=True)
