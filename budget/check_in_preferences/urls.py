from django.contrib import admin
from django.urls import path

from .models import CheckInPreferences

admin.site.register(CheckInPreferences)

url_patterns = []
