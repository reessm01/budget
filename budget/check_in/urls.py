from django.contrib import admin
from django.urls import path

from .models import CheckIn

admin.site.register(CheckIn)

url_patterns = []
