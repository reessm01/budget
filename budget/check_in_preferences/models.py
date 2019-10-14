from django.db import models

from budget.client.models import Client
from budget.frequency.models import Frequency
from budget.account.models import Account
from budget.income.models import Income


class CheckInPreferences(models.Model):
    owner = models.ForeignKey(Client, on_delete=models.CASCADE)

    frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    income = models.ForeignKey(Income, on_delete=models.CASCADE)

    last_modified = models.DateField(auto_now=True, editable=True)
