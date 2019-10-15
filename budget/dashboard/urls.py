from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

url_patterns = [
    path('dashboard/', login_required(Dashboard.as_view()), name='dashboard'),
    path('', login_required(Dashboard.as_view()), name='index'),
    path('dashboard/<id>/', login_required(Dashboard.as_view()), name='dashboard_id')
]
