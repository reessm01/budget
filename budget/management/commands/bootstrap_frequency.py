from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from budget.frequency.models import Frequency


class Command(BaseCommand):
    help = 'Intializes Freqency table with preset values'

    def handle(self, *args, **options):
        frequencies = [
            ('weekly', 52),
            ('bi-monthly', 26),
            ('monthly', 12),
            ('quarterly', 4),
            ('bi-annually', 2),
            ('annually', 1)
        ]

        added = []

        for frequency in frequencies:
            try:
                Frequency.objects.create(
                    title=frequency[0],
                    number_of_paychecks=frequency[1]
                )
                added.append(frequency)
            except IntegrityError:
                continue
            

        self.stdout.write(self.style.SUCCESS(f'Frequency table rows added: {added}'))
