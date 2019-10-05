from django.contrib import admin
from django.urls import path

from .models import Bill

admin.site.register(Bill)

url_patterns = []
