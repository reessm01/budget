from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    started = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
