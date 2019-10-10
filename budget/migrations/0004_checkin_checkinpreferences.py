# Generated by Django 2.2.6 on 2019-10-09 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_auto_20191006_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckInPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Client')),
                ('trace_other', models.ManyToManyField(to='budget.Frequency')),
                ('trace_payday', models.ManyToManyField(to='budget.Income')),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('projected_balance', models.DecimalField(decimal_places=2, max_digits=12)),
                ('actual_balance', models.DecimalField(decimal_places=2, max_digits=12)),
                ('difference', models.DecimalField(decimal_places=2, max_digits=12)),
                ('last_modified', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.Client')),
            ],
        ),
    ]
