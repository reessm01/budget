from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError
import os
import datetime

from budget.bill.models import Bill
from budget.income.models import Income
from budget.account.models import Account
from budget.check_in.models import CheckIn
from budget.check_in.forms import CheckInForm


class Dashboard(TemplateView):

    def get_checkin_info(self, client, entry_id):
        check_ins = CheckIn.objects.filter(user=client).order_by('date')
        selected = ''
        selected_index = -1
        try:
            selected = check_ins.filter(id=entry_id)[0]
            for i, check_in in enumerate(check_ins):
                if check_in.id == entry_id:
                    selected_index = i
                    break
        except (ObjectDoesNotExist, IndexError):
            for i, check_in in enumerate(check_ins):
                if check_in.actual_balance == 0:
                    selected = check_in
                    selected_index = i
                    break
        finally:
            if selected_index + 1 < len(check_ins) and selected_index != -1:
                next_check_in = check_ins[selected_index + 1].id
            else:
                next_check_in = None

            if selected_index - 1 >= 0:
                previous_check_in = check_ins[selected_index - 1].id
            else:
                previous_check_in = None
        return (selected, next_check_in, previous_check_in)

    def chart_serializer(self, datas):
        total = sum([data.amount for data in datas])

        return [{'y': float(data.amount/total*100), 'label': data.title} for data in datas]

    def get_debt_ratio(self, bills, incomes):
        total_income = float(sum([income.amount * income.frequency.number_of_paychecks for income in incomes]))
        total_debts = float(sum([bill.amount * bill.frequency.number_of_paychecks for bill in bills]))
        total_surplus = (total_income - total_debts)/total_income * 100
        total_debts = total_debts / total_income * 100
        return [{
            'y': total_debts,
            'label': 'bills'
        },
        {
            'y': total_surplus,
            'label': 'income'}]

    def get(self, request, *args, **kwargs):
        page = 'dashboard.html'
        user = request.user

        if not user.client.started:
            try:
                bills_completed = Bill.objects.filter(
                    owner=user.client).exists()
                income_completed = Income.objects.filter(
                    owner=user.client).exists()
                accounts_completed = Account.objects.filter(
                    owner=user.client).exists()
                checkins_exist = CheckIn.objects.filter(
                    user=user.client).exists()
                criteria_set_1 = bills_completed and income_completed
                critieria_set_2 = accounts_completed and checkins_exist
                criteria_met = criteria_set_1 and critieria_set_2
                if criteria_met:
                    user.client.started = True
                    user.client.save()
            except Exception:
                return HttpResponseServerError()

        if user.client.started:
            try:
                entry_id = int(self.kwargs['id'])
            except KeyError:
                entry_id = None

            try:
                check_in, next_id, prev_id = self.get_checkin_info(
                    user.client, entry_id)
                form = CheckInForm(checkin_id=check_in.id)
                total_outbound = check_in.futures_balance + check_in.outgoing_balance
                outbound = total_outbound / (check_in.projected_balance)*100
                remaining = 100-outbound
                base_link = '/dashboard/'

                if check_in.date <= datetime.date.today() and check_in.actual_balance == 0.00:
                    subtitle_text_style = 'text-danger'
                else:
                    subtitle_text_style = 'text-muted'

                if next_id is None:
                    next_link = None
                else:
                    next_link = f'{base_link}{next_id}'

                if prev_id is None:
                    prev_link = None
                else:
                    prev_link = f'{base_link}{prev_id}'

                bills_2 = Bill.objects.filter(owner=user.client)
                income = Income.objects.filter(owner=user.client)
                
                bills_data = self.chart_serializer(bills_2)
                debt_ratio_data = self.get_debt_ratio(bills_2, income)
                debt_ratio_chart = {'title': 'debt_ratios', 'data': bills_data}
                income_debt_ratio_chart = {'title': 'income_to_debt_ratios', 'data': debt_ratio_data}
                print(debt_ratio_chart)
                return render(request, page, {
                    'outbound': outbound,
                    'remaining_p': remaining,
                    'check_in': check_in,
                    'total_outbound': total_outbound,
                    'remaining_cash': check_in.projected_balance - total_outbound,
                    'next': next_link,
                    'back': prev_link,
                    'form': form,
                    'subtitle_text_style': subtitle_text_style,
                    'today': datetime.date.today(),
                    'debt_ratio_chart': debt_ratio_chart,
                    'income_debt_ratio_chart': income_debt_ratio_chart
                })
            except Exception as e:
                return HttpResponseServerError()
        else:
            return HttpResponseRedirect(reverse('getting_started'))

    def process_checkin(self, updated_checkin, client):
        check_ins = CheckIn.objects.filter(user=client).order_by('date')

        sentinel = False
        for check_in in check_ins:
            if sentinel:
                check_in.projected_balance += updated_checkin.difference
                check_in.save()
            elif check_in == updated_checkin:
                sentinel = True

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CheckInForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            checkin_id = int(request.POST['checkin_id'])

            try:
                check_in = CheckIn.objects.get(id=checkin_id)
                check_in.actual_balance = data['actual_balance']
                check_in.difference = check_in.actual_balance - check_in.projected_balance
                check_in.save()
                self.process_checkin(check_in, user.client)
            except Exception:
                return HttpResponseServerError()

            return HttpResponseRedirect(f'/dashboard/{checkin_id}')
        else:
            return HttpResponseRedirect(reverse('dashboard'))
