from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db import IntegrityError

from .forms import LoginForm, RegisterForm
from budget.client.models import Client


class logout_client(TemplateView):

    def get(self, request, *args, **kwargs):
        res = HttpResponseRedirect(reverse('login'))
        res.delete_cookie('sessionid')

        return res


class login_client(TemplateView):
    page = 'form.html'
    button_label = 'Submit'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user

        return render(request, self.page, {'user': user, 'form': form, 'button_label': self.button_label})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )

            if user is not None:
                login(request, user)
                destination = request.GET.get('next')

                client = Client.objects.get(user=user)
                if not client.started:
                    return(HttpResponseRedirect(reverse('getting_started')))

                if destination:
                    return(HttpResponseRedirect(destination))
                else:
                    message = 'Login working'
                    return render(request, self.page, {
                        'user': user,
                        'form': form,
                        'button_label': self.button_label,
                        'message': message
                        })
            else:
                error_message = 'Incorrect username or password!'
                return render(request, self.page, {
                    'user': None,
                    'form': form,
                    'button_label': self.button_label,
                    'error_message': error_message
                    })


class register(TemplateView):
    page = 'form.html'
    button_label = 'Lets budget!'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()

        return render(request, self.page, {'user': None, 'form': form, 'button_label': self.button_label})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            try:
                u = User.objects.create_user(
                    username=data['username'],
                    password=data['password'],
                    email=data['email']
                )

                client = Client.objects.create(
                    user=u
                )

                return HttpResponseRedirect(reverse('login'))

            except IntegrityError as error:
                form = RegisterForm()

                return render(request, self.page, {'user': None, 'form': form, 'error_message': error, 'button_label': self.button_label})
