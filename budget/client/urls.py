from django.contrib import admin
from django.urls import path

from .models import Client

admin.site.register(Client)

url_patterns = []
