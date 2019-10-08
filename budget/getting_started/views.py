from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from budget.client.models import Client
from budget.income.models import Income
from budget.income.forms import IncomeForm
from budget.frequency.models import Frequency
from budget.bill.models import Bill
from budget.bill.forms import BillForm
from budget.account.models import Account
from budget.account.forms import AccountForm


class GettingStarted(TemplateView):
    page = 'getting_started.html'

    def get_form(self, end_point):
        form_options = {
            'income': IncomeForm(),
            'bills': BillForm(),
            'accounts': AccountForm()
        }

        return form_options[end_point]

    def get_entries(self, end_point, client):
        entry_options = {
            'income': Income.objects.filter(owner=client),
            'bills': Bill.objects.filter(owner=client),
            'accounts': Account.objects.filter(owner=client)
        }

        return entry_options[end_point]

    def get_next_destination(self, end_point):
        destinations = {
            'income': '/gettingstarted/bills',
            'bills': '/gettingstarted/accounts',
            'accounts': '/dashboard'
        }

        return destinations[end_point]

    def get_prev_destination(self, end_point):
        destinations = {
            'income': None,
            'bills': '/gettingstarted/income',
            'accounts': '/gettingstarted/bills'
        }

        return destinations[end_point]

    def get(self, request, *args, **kwargs):
        user = request.user
        end_point = request.path.split('/')[-1]

        if user:
            client = Client.objects.get(user=user)
            if not client.started:
                form = self.get_form(end_point)
                entries = self.get_entries(end_point, client)
                title = end_point.title()
                button_label = 'Next'
                next_destination = self.get_next_destination(end_point)
                previous_destination = self.get_prev_destination(end_point)

            return render(request, self.page, {
                'title': title,
                'user': user,
                'form': form,
                'entries': entries,
                'button_label': button_label,
                'end_point': end_point.title(),
                'next_destination': next_destination,
                'previous_destination': previous_destination
                })
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_filled_form(self, end_point, data):
        form_options = {
            'income': IncomeForm(data),
            'bills': BillForm(data),
            'accounts': AccountForm(data)
        }

        return form_options[end_point]

    def create_entry(self, data, client, end_point):
        if end_point == 'income':
            Income.objects.create(
                owner=client,
                title=data['title'],
                amount=data['amount'],
                frequency=data['frequency'],
                last_paid=data['last_paid']
                )
        elif end_point == 'bills':
            Bill.objects.create(
                owner=client,
                title=data['title'],
                amount=data['amount'],
                frequency=data['frequency'],
                last_paid=data['last_paid'],
                weekdays_only=data['weekdays_only']
                )
        elif end_point == 'accounts':
            Account.objects.create(
                owner=client,
                title=data['title'],
                amount=data['amount'],
                account_type=data['account_type']
            )

    def post(self, request, *args, **kwargs):
        user = request.user

        if user:
            end_point = request.path.split('/')[-1]
            form = self.get_filled_form(end_point, request.POST)

            if form.is_valid():
                client = Client.objects.get(user=user)
                data = form.cleaned_data

                self.create_entry(data, client, end_point)

                return HttpResponseRedirect(request.path)
