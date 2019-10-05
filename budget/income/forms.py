from django import forms

from budget.frequency.models import Frequency


class IncomeForm(forms.Form):
    title = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=9, decimal_places=2)
    frequency = forms.ModelChoiceField(queryset=Frequency.objects.all())
    last_paid = forms.DateField(widget=forms.SelectDateWidget)
