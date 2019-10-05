from django.contrib import admin
from django.urls import path

from .views import *

url_patterns = [
    path('login', login_client.as_view(), name='login'),
    path('register', register.as_view(), name='register'),
    path('logout', logout_client.as_view(), name='logout')
]
