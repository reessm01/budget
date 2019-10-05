from django.contrib import admin
from django.urls import path

from .models import Account

admin.site.register(Account)

url_patterns = []
