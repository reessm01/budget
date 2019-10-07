from django.contrib import admin
from django.urls import path

from .views import *

url_patterns = [
    path(
        'gettingstarted/income',
        GettingStarted.as_view(),
        name='getting_started'
        ),
    path(
        'gettingstarted/bills',
        GettingStarted.as_view(),
        name='getting_started_bills'
        ),
    path(
        'gettingstarted/accounts',
        GettingStarted.as_view(),
        name='getting_started_accounts'
        ),
]
