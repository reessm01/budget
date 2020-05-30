from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseServerError
from datetime import timedelta
from calendar import monthrange
from decimal import Decimal

from budget.client.models import Client
from budget.income.models import Income
from budget.income.forms import IncomeForm
from budget.frequency.models import Frequency
from budget.bill.models import Bill
from budget.bill.forms import BillForm
from budget.account.models import Account, AccountType
from budget.account.forms import AccountForm
from budget.check_in_preferences.models import CheckInPreferences
from budget.check_in_preferences.forms import CheckInPreferencesForm
from budget.check_in.models import CheckIn


class InitCheckinPreferences(TemplateView):

    def get_reserve_ratio(self, bill, next_check_in, time_delta, sequence):
        bill_next_due = bill.next_due()
        date_difference = bill_next_due - next_check_in
        while date_difference.days < 0:
            bill_next_due = bill.next_due(bill_next_due)
            date_difference = bill_next_due - next_check_in

        ratio = Decimal(0.00)
        while next_check_in <= bill_next_due < next_check_in + time_delta:
            ratio += Decimal(1.00)
            bill_next_due = bill.next_due(bill_next_due)

        offset = Decimal(0.00)
        if next_check_in + time_delta <= bill_next_due < next_check_in + time_delta*2:
            diff = (bill_next_due - next_check_in + time_delta).days
            if bill.days_between() - diff > 0:
                offset = Decimal(
                    (bill.days_between() - diff)/bill.days_between())

        return (ratio, offset)

    def account_balance_projection(self, bills, balance, next_checkin_date, account, time_delta, sequence, income):
        reserve = Decimal(0.00)
        outgoing = Decimal(0.00)

        for bill in bills:
            reserve_ratio = self.get_reserve_ratio(
                bill, next_checkin_date, time_delta, sequence
            )

            outgoing += bill.amount * reserve_ratio[0]
            reserve += bill.amount * reserve_ratio[1]

        for entry in income:
            next_paid = entry.next_paid()
            date_difference = entry.next_paid() - next_checkin_date
            while date_difference.days < 0:
                next_paid = entry.next_paid(next_paid)
                date_difference = next_paid - next_checkin_date
            while next_checkin_date <= next_paid < next_checkin_date + time_delta:
                balance += entry.amount
                next_paid = entry.next_paid(next_paid)

        transaction = {
            'date': next_checkin_date,
            'projected_balance': balance,
            'futures_balance': reserve,
            'outgoing_balance': outgoing
        }

        return transaction

    def get(self, request, *args, **kwargs):
        user = request.user
        page = 'getting-started/components/archive/init_check_preferences.component.html'
        form = CheckInPreferencesForm(client=user.client)

        return render(request, page, {
            'title': 'Check-in Configuration',
            'user': user,
            'form': form,
            'guidance': 'Please indicate the frequency you would like to check in. Check ins are automated events that runs a comparison between your projected account and actual account balances.',
            'button_label': 'Submit',
            'next_destination': '/dashboard',
            'previous_destination': '/gettingstarted/accounts'
        })
        # else:
        #     return HttpResponseRedirect(reverse('index'))

    def get_time_delta(self, preferences, last_paid):
        if preferences.frequency.title == 'monthly':
            time_delta = timedelta(
                monthrange(
                    last_paid.year, last_paid.month)[1]
            )
        else:
            time_delta = timedelta(
                days=365 // preferences.frequency.number_of_paychecks)

        return time_delta

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CheckInPreferencesForm(request.POST, {'client': user.client})

        if form.is_valid():
            data = form.cleaned_data

            try:
                preferences = CheckInPreferences.objects.get(owner=user.client)
                preferences.frequency = data['frequency']
                preferences.account = data['account']
                preferences.income = data['income']
                preferences.save()

            except ObjectDoesNotExist:
                preferences = CheckInPreferences.objects.create(
                    owner=user.client,
                    frequency=data['frequency'],
                    account=data['account'],
                    income=data['income']
                )

            except Exception:
                return HttpResponseServerError()

            finally:
                try:
                    CheckIn.objects.filter(user=user.client).delete()
                    time_delta = self.get_time_delta(
                        preferences, preferences.income.last_paid)

                    next_date = preferences.income.last_paid + time_delta
                    bills = Bill.objects.filter(owner=user.client)
                    income = Income.objects.filter(owner=user.client)
                    check_ins = []
                    for sequence in range(
                            1, preferences.frequency.number_of_paychecks + 1
                    ):
                        if sequence != 1:
                            time_delta = self.get_time_delta(
                                preferences, check_ins[-1]['date'])
                            next_date = check_ins[-1]['date'] + time_delta
                            account_balance = check_ins[-1]['projected_balance'] - \
                                check_ins[-1]['outgoing_balance']
                        else:
                            account_balance = preferences.account.amount
                        check_ins.append(self.account_balance_projection(
                            bills, account_balance, next_date,
                            preferences.account, time_delta, sequence, income
                        ))

                    for check_in in check_ins:
                        CheckIn.objects.create(
                            user=user.client,
                            date=check_in['date'],
                            projected_balance=check_in['projected_balance'],
                            futures_balance=check_in['futures_balance'],
                            outgoing_balance=check_in['outgoing_balance']
                        )
                except Exception:
                    return HttpResponseServerError()

            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('check_in'))


class GettingStartedLanding(TemplateView):
    page = 'getting-started/landing.page.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.page, {})


class GettingStartedNewEntry(TemplateView):
    page = 'getting-started/getting_started.page.html'

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

    def get_filled_form(self, end_point, data):
        form_options = {
            'income': IncomeForm(data),
            'bills': BillForm(data),
            'accounts': AccountForm(data)
        }

        return form_options[end_point]

    def post(self, request, *args, **kwargs):
        user = request.user

        if user:
            try:
                end_point = request.path.split('/')[-1]
                redirect_path = '/gettingstarted/{0}'.format(end_point)

                form = self.get_filled_form(end_point, request.POST)
                if form.is_valid():
                    client = Client.objects.get(user=user)
                    data = form.cleaned_data
                    self.create_entry(data, client, end_point)

                    return HttpResponseRedirect(redirect_path)
            except Exception as e:
                print(e)
                return HttpResponseServerError()

        return HttpResponseRedirect(reverse('getting_started'))


class GettingStarted(TemplateView):
    page = 'getting-started/getting_started.page.html'

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

    def get_model(self, end_point, entry_id, client):
        entry_options = {
            'income': Income.objects.filter(owner=client).filter(id=entry_id),
            'bills': Bill.objects.filter(owner=client).filter(id=entry_id),
            'accounts': Account.objects.filter(owner=client).filter(id=entry_id)
        }
        return entry_options[end_point]

    def get_a_form(self, end_point, initial_data):
        if end_point == 'income':
            initial_choice = initial_data['frequency_id']
            new_choice = {
                'frequency': Frequency.objects.filter(pk=initial_choice)[0]}
            initial_data.update(new_choice)

            return IncomeForm(initial=initial_data)
        elif end_point == 'bills':
            initial_choice = initial_data['frequency_id']
            new_choice = {
                'frequency': Frequency.objects.filter(pk=initial_choice)[0]}
            initial_data.update(new_choice)

            return BillForm(initial=initial_data)
        elif end_point == 'accounts':

            initial_choice = initial_data['account_type_id']
            new_choice = {
                'account_type': AccountType.objects.filter(pk=initial_choice)[0]}
            initial_data.update(new_choice)

            return AccountForm(initial=initial_data)

    def get(self, request, *args, **kwargs):
        user = request.user
        end_point = request.path.split('/')[-1]

        if user:
            client = Client.objects.get(user=user)
            # if client.started:
            form = self.get_form(end_point)
            entries = self.get_entries(end_point, client)
            title = end_point.title()
            button_label = 'Next'
            next_destination = self.get_next_destination(end_point)
            previous_destination = self.get_prev_destination(end_point)

            forms = []
            for entry in entries:
                init_data = self.get_model(
                    end_point, entry.pk, user.client)
                forms.append(self.get_a_form(
                    end_point, init_data.values()[0]))
            return render(request, self.page, {
                'title': title,
                'user': user,
                'form': form,
                'entries': entries,
                'forms': forms,
                'button_label': button_label,
                'end_point': end_point.title(),
                'next_destination': next_destination,
                'previous_destination': previous_destination
            })
            # else:
            #     return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_filled_form(self, end_point, data):
        form_options = {
            'income': IncomeForm(data),
            'bills': BillForm(data),
            'accounts': AccountForm(data)
        }

        return form_options[end_point]

    def change_info(self, data, client, end_point, id):
        if end_point == 'income':
            Income.objects.filter(id=id).update(

                title=data['title'],
                amount=data['amount'],
                frequency=data['frequency'],
                last_paid=data['last_paid']
            )

        elif end_point == 'bills':
            Bill.objects.filter(id=id).update(

                title=data['title'],
                amount=data['amount'],
                frequency=data['frequency'],
                last_paid=data['last_paid'],
                weekdays_only=data['weekdays_only']
            )

        elif end_point == 'accounts':
            Account.objects.filter(id=id).update(

                title=data['title'],
                amount=data['amount'],
                account_type=data['account_type']
            )

    def delete_entry(self, id, end_point):
        if end_point == 'income':
            Income.objects.get(pk=id).delete()
        elif end_point == 'bills':
            Bill.objects.get(pk=id).delete()
        elif end_point == 'accounts':
            Account.objects.get(pk=id).delete()

    def delete(self, request, id, *args, **kwargs):
        user = request.user
        if user:
            try:
                end_point = request.path.split('/')[-2]
                self.delete_entry(id, end_point)
                return HttpResponse(200)
            except Exception as e:
                print(e)
                return HttpResponseServerError()

        return HttpResponseRedirect(reverse('getting_started'))

    def post(self, request, id, *args, **kwargs):
        user = request.user
        if user:
            try:
                end_point = request.path.split('/')[-2]
                form = self.get_filled_form(end_point, request.POST)
                if form.is_valid():
                    client = Client.objects.get(user=user)
                    data = form.cleaned_data

                    self.change_info(data, client, end_point, int(id))
                    redirect = '/'.join(request.path.split('/')[:-1])
                    return HttpResponseRedirect(redirect)
            except Exception as e:
                print(e)
                return HttpResponseServerError()

        return HttpResponseRedirect(reverse('getting_started'))
