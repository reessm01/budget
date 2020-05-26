from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from budget.account.models import AccountType


class Command(BaseCommand):
    help = 'Intializes AccountType table with preset values'

    def handle(self, *args, **options):
        account_types = [
            'checking',
            'reserve',
            'savings',
            'credit card',
            'loan',
            'retirement',
            'other'
        ]

        added = []

        for account_type in account_types:
            try:
                entry = AccountType.objects.filter(title=account_type)
                if not entry.exists():
                    AccountType.objects.create(
                        title=account_type,
                    )
                    added.append(account_type)
            except IntegrityError:
                continue

        self.stdout.write(
            self.style.SUCCESS(f'AccountType table rows added: {added}')
            )
