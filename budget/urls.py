from django.contrib import admin
from django.urls import path

from budget.check_in_preferences.urls import url_patterns as check_in_preferences_urls
from budget.check_in.urls import url_patterns as check_in_urls
from budget.dashboard.urls import url_patterns as dashboard_urls
from budget.getting_started.urls import url_patterns as getting_started_urls
from budget.auth.urls import url_patterns as auth_urls
from budget.transaction_log.urls import url_patterns as transaction_log_urls
from budget.transaction.urls import url_patterns as transaction_urls
from budget.frequency.urls import url_patterns as frequency_urls
from budget.account.urls import url_patterns as account_urls
from budget.income.urls import url_patterns as income_urls
from budget.client.urls import url_patterns as client_urls
from budget.bill.urls import url_patterns as bill_urls
from django.shortcuts import render
import os


def error_404(request, exception):
    return render(request, 'http/404.html', status=404)


def error_500(request):
    return render(request, 'http/500.html', status=500)


handler404 = error_404
handler500 = error_500

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += client_urls
urlpatterns += bill_urls
urlpatterns += income_urls
urlpatterns += account_urls
urlpatterns += frequency_urls
urlpatterns += transaction_urls
urlpatterns += transaction_log_urls
urlpatterns += auth_urls
urlpatterns += getting_started_urls
urlpatterns += dashboard_urls
urlpatterns += check_in_urls
urlpatterns += check_in_preferences_urls
