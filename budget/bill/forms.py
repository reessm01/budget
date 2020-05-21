from django import forms

from budget.frequency.models import Frequency


class BillForm(forms.Form):
    title = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=9, decimal_places=2)
    frequency = forms.ModelChoiceField(queryset=Frequency.objects.all())
    last_paid = forms.DateField(widget=forms.DateInput(
        format='%m/%d/%Y',
        attrs={'placeholder': '03/31/1989'}),
        input_formats=['%m/%d/%Y', ]
    )
    weekdays_only = forms.BooleanField(initial=True, required=False)
