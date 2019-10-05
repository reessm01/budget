from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from budget.client.models import Client
from budget.income.models import Income
from budget.income.forms import IncomeForm
from budget.frequency.models import Frequency


class GettingStarted(TemplateView):
    page = 'getting_started_income.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user:
            client = Client.objects.get(user=user)
            if not client.started:
                form = IncomeForm()
                income = Income.objects.filter(owner=client)
                total = sum([entry.amount for entry in income])
                button_label = 'Next'

            return render(request, self.page, {
                'user': user,
                'form': form,
                'income': income,
                'total': total,
                'button_label': button_label
                })
        else:
            return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        user = request.user

        if user:
            form = IncomeForm(request.POST)

            if form.is_valid():
                client = Client.objects.get(user=user)
                data = form.cleaned_data

                Income.objects.create(
                    owner=client,
                    title=data['title'],
                    amount=data['amount'],
                    frequency=data['frequency'],
                    last_paid=data['last_paid']
                )

                return HttpResponseRedirect(reverse('getting_started'))
