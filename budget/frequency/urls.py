from django.contrib import admin
from django.urls import path

from .models import Frequency

admin.site.register(Frequency)

url_patterns = []
