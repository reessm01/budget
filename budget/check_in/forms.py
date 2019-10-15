from django import forms

from budget.check_in.models import CheckIn
    # user = models.ForeignKey(Client, on_delete=models.CASCADE)
    # date = models.DateField(editable=True)
    # projected_balance = models.DecimalField(max_digits=12, decimal_places=2)
    # futures_balance = models.DecimalField(max_digits=12, decimal_places=2)
    # outgoing_balance = models.DecimalField(max_digits=12, decimal_places=2)
    # actual_balance = models.DecimalField(
    #     max_digits=12,
    #     decimal_places=2,
    #     default=0.00
    #     )
    # difference = models.DecimalField(
    #     max_digits=12,
    #     decimal_places=2,
    #     default=0.00
    #     )
class CheckInForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        checkin_id = kwargs.pop('checkin_id', None)
        super().__init__(*args, **kwargs)

        if checkin_id:
            self.fields['checkin_id'] = forms.IntegerField(
                initial=checkin_id)

    class Meta:
        model = CheckIn
        fields = [
            'actual_balance'
        ]
