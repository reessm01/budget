from django.contrib import admin
from django.urls import path

from .models import Income

admin.site.register(Income)

url_patterns = []
