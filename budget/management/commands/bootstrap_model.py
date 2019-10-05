from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Bootstraps basic model and adds it to baseapps urls.py file'

    def add_arguments(self, parser):
        parser.add_argument(
            'model',
            type=str,
            help='Model name to be initialized.'
            )

    def handle(self, *args, **options):
        app_name = 'budget'
        basename = options['model']
        path = f'./{app_name}/{basename}'
        views_content = 'from django.shortcuts import render, HttpResponseRedirect, reverse\nfrom django.contrib.auth.decorators import login_required'
        if not os.path.exists(path):
            os.mkdir(path)
            with open(f'{path}/__init__.py', 'w+'):
                pass
            with open(f'{path}/models.py', 'w+') as f:
                f.write('from django.db import models')
            with open(f'{path}/forms.py', 'w+') as f:
                f.write('from django import forms')
            with open(f'{path}/urls.py', 'a+') as f:
                f.write('from django.contrib import admin\n')
                f.write('from django.urls import path\n\n')
                f.write('url_patterns = []\n')
            with open(f'{path}/views.py', 'w+') as f:
                f.write(views_content)

            content = []
            with open(f'./{app_name}/urls.py', 'r') as f:
                content = f.readlines()

            content.insert(
                3,
                f'from {app_name}.{basename}.urls import url_patterns as {basename}_urls\n'
                )
            content.append(f'urlpatterns += {basename}_urls\n')

            with open(f'./{app_name}/urls.py', 'w') as f:
                contents = ''.join(content)
                f.write(contents)
