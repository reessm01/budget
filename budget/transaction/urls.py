from django.contrib import admin
from django.urls import path

from .models import Transaction

admin.site.register(Transaction)

url_patterns = []
