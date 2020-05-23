from django.core.management.base import BaseCommand
from django.core import management
import subprocess


class Command(BaseCommand):
    help = 'Initializes the project running common commands in a single line.'

    def handle(self, *args, **options):
        management.call_command('makemigrations')
        management.call_command('migrate')
        management.call_command('bootstrap_account_type')
        management.call_command('bootstrap_frequency')
        subprocess.run(['npm', 'run', 'init'])
        self.stdout.write(self.style.SUCCESS('Finished initializing project!'))
