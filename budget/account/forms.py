from django import forms

from .models import Account, AccountType


class AccountForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        queryset=AccountType.objects.all(),
        widget=forms.Select()
    )

    class Meta:
        model = Account
        fields = [
            'title',
            'account_type',
            'amount',
        ]
