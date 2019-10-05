from django import forms


class IncomeForm(forms.Form):
    title = forms.CharField(max_length=100)
    amount = forms.DecimalField(max_digits=9, decimal_places=2)
    frequency = forms.ModelChoiceField(queryset=Frequency.objects.all())
    last_paid = forms.DateField(widget=forms.SelectDateWidget)

# class Bill(models.Model):
#     owner = models.ForeignKey(Client, on_delete=models.CASCADE)

#     title = models.CharField(max_length=50)
#     amount = models.DecimalField(max_digits=9, decimal_places=2)
#     day_due = models.IntegerField()
#     weekdays_only = models.BooleanField(default=True)

#     last_modified = models.DateField(auto_now=True, editable=True)