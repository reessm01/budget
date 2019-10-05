from django.db import models


class Frequency(models.Model):
    title = models.CharField(max_length=50, unique=True)
    number_of_paychecks = models.IntegerField()

    def __str__(self):
        return self.title
