from django import forms

from .models import CheckInPreferences
from budget.income.models import Income
from budget.frequency.models import Frequency
from budget.account.models import Account


class CheckInPreferencesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CheckInPreferencesForm, self).__init__(*args, **kwargs)
        client = kwargs.pop('client', None)
        if client:
            self.account_type = forms.ModelChoiceField(
                queryset=Account.objects.filter(owner=client),
                widget=forms.Select()
            )

    frequency = forms.ModelChoiceField(
        queryset=Frequency.objects.all(),
        widget=forms.Select()
    )

    class Meta:
        model = CheckInPreferences
        fields = [
            'frequency',
            'account',
        ]
