from django.contrib import admin
from django.urls import path

from .views import *

url_patterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('chart', Chart.as_view(), name='chart')
]
