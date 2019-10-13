from django.db import models
from datetime import datetime, timedelta, date
from calendar import monthrange


class Frequency(models.Model):
    title = models.CharField(max_length=50, unique=True)
    number_of_paychecks = models.IntegerField()

    def __str__(self):
        return self.title
