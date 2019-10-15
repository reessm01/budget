from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
import os
import datetime

from budget.bill.models import Bill
from budget.income.models import Income
from budget.account.models import Account
from budget.check_in.models import CheckIn
from budget.check_in.forms import CheckInForm


class Dashboard(TemplateView):
    def save_chart(self, user, total, sizes, labels, path):
        import matplotlib
        matplotlib.use('TkAgg')
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        explode = [0 if size >= 0.05 else 0.25 for size in sizes]
        fig1, ax1 = plt.subplots()
        wedges, _ = ax1.pie(sizes, explode=explode, shadow=True)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')
        labels = [
            '{0} - {1:1.1f} %'.format(label, size*100)
            for label, size in zip(labels, sizes)
        ]
        ax1.legend(
            wedges,
            labels,
            loc='center left',
            bbox_to_anchor=(1, 0, 0.5, 1),
            prop=dict(size=16)
        )
        ax1.axes.get_xaxis().set_visible(False)
        ax1.axes.get_yaxis().set_visible(False)

        plt.subplots_adjust(
            top=1,
            bottom=0,
            right=1,
            left=0,
            hspace=0,
            wspace=0
        )
        plt.margins(0, 0)
        plt.rcParams['legend.title_fontsize'] = 'large'

        plt.savefig(
            path,
            bbox_inches='tight',
            dpi=100,
            quality=100,
            pad_inches=0.015
        )

    def process_previous_filename(self, user, title, image_directory, path, remove):
        previous_filename = ''
        for image in image_directory:
            if f'{user.id}_{title}' in image:
                previous_filename = image
                break

        if previous_filename and remove:
            os.remove(path + previous_filename)

        return previous_filename

    def create_charts(self, user):
        path = './budget/static/img/'
        image_directory = os.listdir(path)
        chart_info = [
            ('bills', Bill.objects.filter(owner=user.client)),
            ('income', Income.objects.filter(owner=user.client))
        ]

        images = []

        for chart in chart_info:
            title, query = chart[0], chart[1].order_by('-amount')
            last_modified = [
                entry.last_modified
                for entry in query.order_by('-last_modified')
            ][0]
            filename = f'{user.id}_{title}_{last_modified}.png'
            
            if filename not in image_directory:
                previous_filename = self.process_previous_filename(
                    user, title, image_directory, path, True)
                if not previous_filename:
                    if title == 'bills':
                        total = sum([entry.amount for entry in query])
                        sizes = [entry.amount/total for entry in query]
                        labels = [entry.title for entry in query]
                        self.save_chart(user, total, sizes, labels, path + filename)
                    else:
                        income_total = sum([entry.amount*entry.frequency.number_of_paychecks for entry in query])
                        bills_total = sum([
                            entry.amount*entry.frequency.number_of_paychecks for entry in chart_info[0][1]
                            ])
                        total = income_total + bills_total
                        sizes = [
                            entry/total
                            for entry in [income_total, bills_total]
                            ]
                        labels = [entry for entry in ['income', 'bills']]
                        self.save_chart(user, total, sizes, labels, path + filename)
                    images.append('img/' + filename)
                else:
                    images.append('img/' + previous_filename)

            else:
                previous_filename = self.process_previous_filename(
                    user, title, image_directory, path, False)
                images.append('img/' + previous_filename)

        return images

    def get_checkin_info(self, client, entry_id):
        check_ins = CheckIn.objects.filter(user=client).order_by('date')
        selected = ''
        selected_index = -1
        previous_index = -1
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

    def get(self, request, *args, **kwargs):
        page = 'dashboard.html'
        user = request.user

        if not user.client.started:
            bills_completed = Bill.objects.filter(
                owner=user.client).exists()
            income_completed = Income.objects.filter(
                owner=user.client).exists()
            accounts_completed = Account.objects.filter(
                owner=user.client).exists()
            checkins_exist = Checkin.objects.filter(
                user=user.client).exists()
            criteria_set_1 = bills_completed and income_completed
            critieria_set_2 = accounts_completed and checkins_exist
            criteria_met = criteria_set_1 and critieria_set_2
            if criteria_met:
                user.client.started = True
                user.client.save()

        if user.client.started:
            try:
                entry_id = int(self.kwargs['id'])
            except KeyError:
                entry_id = None

            form = CheckInForm()
            file_paths = self.create_charts(user)
            bills, incomes = file_paths[0], file_paths[1]
            check_in, next_id, prev_id = self.get_checkin_info(user.client, entry_id)
            total_outbound = check_in.futures_balance + check_in.outgoing_balance
            outbound = total_outbound / (check_in.projected_balance)*100
            remaining = 100-outbound
            base_link = '/dashboard/'

            if check_in.date <= datetime.date.today():
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
            return render(request, page, {
                'bills': bills,
                'incomes': incomes,
                'outbound': outbound,
                'remaining_p': remaining,
                'check_in': check_in,
                'total_outbound': total_outbound,
                'remaining_cash': check_in.projected_balance - total_outbound,
                'next': next_link,
                'back': prev_link,
                'form': form,
                'subtitle_text_style': subtitle_text_style,
                'today': datetime.date.today()
            })
        else:
            return HttpResponseRedirect(reverse('getting_started'))
