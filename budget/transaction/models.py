from django.db import models

from budget.client.models import Client


class Transaction(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateField(auto_now_add=True)
