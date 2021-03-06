from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

url_patterns = [
    path(
        'settings',
        login_required(GettingStartedLanding.as_view()),
        name='settings'
    ),
    path(
        'gettingstarted/checkin',
        login_required(InitCheckinPreferences.as_view()),
        name='check_in'
    ),
    path(
        'gettingstarted/income',
        login_required(GettingStarted.as_view()),
        name='getting_started'
    ),
    path(
        'gettingstarted/bills',
        login_required(GettingStarted.as_view()),
        name='getting_started_bills'
    ),
    path(
        'gettingstarted/accounts',
        login_required(GettingStarted.as_view()),
        name='getting_started_accounts'
    ),
    path(
        'gettingstarted/income/<int:id>',
        login_required(GettingStarted.as_view()),
        name='edit_getting_started_income'
    ),
    path(
        'gettingstarted/bills/<int:id>',
        login_required(GettingStarted.as_view()),
        name='edit_getting_started_bills'
    ),
    path(
        'gettingstarted/accounts/<int:id>',
        login_required(GettingStarted.as_view()),
        name='_edit_getting_started_accounts'
    ),
    path(
        'gettingstarted/new/income',
        login_required(GettingStartedNewEntry.as_view()),
        name='new_getting_started_income'
    ),
    path(
        'gettingstarted/new/bills',
        login_required(GettingStartedNewEntry.as_view()),
        name='new_getting_started_bills'
    ),
    path(
        'gettingstarted/new/accounts',
        login_required(GettingStartedNewEntry.as_view()),
        name='new_getting_started_accounts'
    ),
]
