# Generated by Django 2.2.6 on 2019-10-12 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20191010_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='futures_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checkin',
            name='outgoing_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
            preserve_default=False,
        ),
    ]
