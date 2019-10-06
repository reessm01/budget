from django.shortcuts import render, HttpResponseRedirect, reverse, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
