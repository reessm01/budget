from django.contrib import admin
from django.urls import path

from .models import Account, AccountType

admin.site.register(Account)
admin.site.register(AccountType)

url_patterns = []
