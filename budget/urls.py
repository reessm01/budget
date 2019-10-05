from django.contrib import admin
from django.urls import path

from budget.getting_started.urls import url_patterns as getting_started_urls
from budget.auth.urls import url_patterns as auth_urls
from budget.transaction_log.urls import url_patterns as transaction_log_urls
from budget.transaction.urls import url_patterns as transaction_urls
from budget.frequency.urls import url_patterns as frequency_urls
from budget.account.urls import url_patterns as account_urls
from budget.income.urls import url_patterns as income_urls
from budget.client.urls import url_patterns as client_urls
from budget.bill.urls import url_patterns as bill_urls

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
