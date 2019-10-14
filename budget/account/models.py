from django.db import models

from budget.client.models import Client


class AccountType(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Account(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE,
        null=True
        )

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    created = models.DateField(auto_now_add=True)

    def get_attributes(self):
        return [
            'title',
            'account_type',
            'amount',
        ]

    def __str__(self):
        return self.title
