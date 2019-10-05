from django.db import models


class Frequency(models.Model):
    title = models.CharField(max_length=50)
    number_of_paychecks = models.IntegerField()
