from django.db import models

from budget.client.models import Client


class Account(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    is_bank = models.BooleanField(default=False)

    created = models.DateField(auto_now_add=True)
