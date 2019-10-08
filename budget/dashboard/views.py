from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):
        page = 'dashboard.html'

        return render(request, page, {})


class Chart(TemplateView):
    def get(self, request, *args, **kwargs):
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt

        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        sizes = [15, 30, 45, 10]
        explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

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
