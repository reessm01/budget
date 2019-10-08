from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from budget.bill.models import Bill


class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):
        page = 'dashboard.html'

        return render(request, page, {})


class Chart(TemplateView):
    def get(self, request, *args, **kwargs):
        import matplotlib
        matplotlib.use('TkAgg')
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        user = request.user
        bills = Bill.objects.filter(owner=user.client)
        total = sum([bill.amount for bill in bills])

        sizes = [bill.amount/total for bill in bills]
        labels = [bill.title for bill in bills]
        explode = [0 if size >= 0.05 else 0.5 for size in sizes]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        jpeg = plt.savefig(
            './budget/static/img/foo.png',
            bbox_inches='tight',
            dpi=100,
            quality=100
            )

        return HttpResponse('budget/foo.png', content_type="image/png")
