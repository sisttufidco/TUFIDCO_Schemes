# Generated by Django 4.0 on 2022-02-03 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0109_delete_testmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
            ],
            options={
                'verbose_name': 'Dashboard',
                'verbose_name_plural': 'Dashboards',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('TUFIDCOapp.mastersanctionform',),
        ),
    ]
