from django.contrib import admin
from django.urls import path

from .views import *

url_patterns = [
    path(
        'gettingstarted/checkin',
        InitCheckinPreferences.as_view(),
        name='check_in'
    ),
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
    path(
        'gettingstarted/income/<int:id>',
        GettingStartedEdit.as_view(),
        name='edit_getting_started'
    ),
    path(
        'gettingstarted/bills/<int:id>',
        GettingStartedEdit.as_view(),
        name='edit_getting_started_bills'
    ),
    path(
        'gettingstarted/accounts/<int:id>',
        GettingStartedEdit.as_view(),
        name='_edit_getting_started_accounts'
    ),
]
