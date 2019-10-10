# Generated by Django 2.2.6 on 2019-10-10 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_checkin_checkinpreferences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkinpreferences',
            name='trace_other',
        ),
        migrations.RemoveField(
            model_name='checkinpreferences',
            name='trace_payday',
        ),
        migrations.AddField(
            model_name='checkinpreferences',
            name='frequency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='budget.Frequency'),
            preserve_default=False,
        ),
    ]
