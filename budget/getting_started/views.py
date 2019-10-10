from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from budget.client.models import Client
from budget.income.models import Income
from budget.income.forms import IncomeForm
from budget.frequency.models import Frequency
from budget.bill.models import Bill
from budget.bill.forms import BillForm
from budget.account.models import Account
from budget.account.forms import AccountForm
from budget.check_in_preferences.models import CheckInPreferences
from budget.check_in_preferences.forms import CheckInPreferencesForm
from budget.check_in.models import CheckIn


class InitCheckinPreferences(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        page = 'init_check_preferences.html'
        form = CheckInPreferencesForm({'client': user.client})

        return render(request, page, {
            'title': 'Check-in Configuration',
            'user': user,
            'form': form,
            'guidance': 'Please indicate the frequency you would like to check in. Check ins are automated events that runs a comparison between your projected account and actual account balances.',
            'button_label': 'Submit',
            'next_destination': '/dashboard',
            'previous_destination': '/gettingstarted/accounts'
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CheckInPreferencesForm(request.POST, {'client': user.client})

        if form.is_valid():
            data = form.cleaned_data

            try:
                preferences = CheckInPreferences.objects.get(owner=user.client)
                preferences.frequency = data['frequency']
                preferences.account = data['account']
                preferences.save()
            except ObjectDoesNotExist:
                preferences = CheckInPreferences.objects.create(
                    owner=user.client,
                    frequency=data['frequency'],
                    account=data['account']
                )
            finally:
                pass
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            HttpResponseRedirect(reverse('check_in'))


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
            'accounts': '/gettingstarted/checkin'
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
            if client.started:
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


class GettingStartedEdit(TemplateView):
    page = 'getting_started_edit.html'

    def get_form(self, end_point, initial_data):
        print(initial_data)
        if end_point == 'income':
            return IncomeForm(initial=initial_data)
        elif end_point == 'bills':
            return BillForm(initial=initial_data)
        elif end_point == 'accounts':
            return AccountForm(initial=initial_data)
        # form_options = {
        #     'income': IncomeForm(initial=initial_data),
        #     'bills': BillForm(initial=initial_data),
        #     'accounts': AccountForm(initial=initial_data)
        # }
        # return form_options[end_point]

    def get(self, request, id, *args, **kwargs):
        user = request.user
        end_point = request.path.split('/')[-2]

        if user:
            client = Client.objects.get(user=user)
            if not client.started:
                initial_data = self.get_model(end_point, id)
                # print(initial_data)
                form = self.get_form(end_point, initial_data.values()[0])
                # entries = self.get_entries(end_point, client)
                title = end_point.title()
                # button_label = 'Next'
                # next_destination = self.get_next_destination(end_point)
                # previous_destination = self.get_prev_destination(end_point)

            return render(request, self.page, {
                'title': title,
                'user': user,
                'form': form,
                # 'entries': entries,
                # 'button_label': button_label,
                'end_point': end_point.title(),
                # 'next_destination': next_destination,
                # 'previous_destination': previous_destination
            })
        else:
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, id, *args, **kwargs):
        user = request.user

        if user:
            end_point = request.path.split('/')[-2]
            print(end_point, request.POST)
            form = self.get_filled_form(end_point, request.POST)

            if form.is_valid():
                client = Client.objects.get(user=user)
                data = form.cleaned_data

                self.change_info(data, client, end_point, id)
                redirect_path = request.path.split('/')[:-1]
                return HttpResponseRedirect("/".join(redirect_path))

    def change_info(self, data, client, end_point, id):
        if end_point == 'income':
            Income.objects.filter(id=id).update(

                title=data['title'],
                amount=data['amount'],
                frequency=data['frequency'],
                last_paid=data['last_paid']
            )
            # Income.save()
        elif end_point == 'bills':
            Bill.objects.filter(id=id).update(

                title=data['title'],
                amount=data['amount'],
                frequency=data['frequency'],
                last_paid=data['last_paid'],
                weekdays_only=data['weekdays_only']
            )
            # Bill.save()
        elif end_point == 'accounts':
            Account.filter(id=id).update(

                title=data['title'],
                amount=data['amount'],
                account_type=data['account_type']
            )
            # Account.save()

    def get_model(self, end_point, id):
        entry_options = {
            'income': Income.objects.filter(id=id),
            'bills': Bill.objects.filter(id=id),
            'accounts': Account.objects.filter(id=id)
        }
        return entry_options[end_point]

    def get_filled_form(self, end_point, data):
        form_options = {
            'income': IncomeForm(data),
            'bills': BillForm(data),
            'accounts': AccountForm(data)
        }
        return form_options[end_point]
