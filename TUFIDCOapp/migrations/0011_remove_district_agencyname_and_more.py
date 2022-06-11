# Generated by Django 4.0 on 2021-12-31 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0010_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='AgencyName',
        ),
        migrations.RemoveField(
            model_name='mastersanctionform',
            name='AgencyName',
        ),
        migrations.RemoveField(
            model_name='mastersanctionform',
            name='AgencyType',
        ),
        migrations.RemoveField(
            model_name='mastersanctionform',
            name='District',
        ),
        migrations.RemoveField(
            model_name='mastersanctionform',
            name='Region',
        ),
        migrations.RemoveField(
            model_name='region',
            name='District',
        ),
        migrations.DeleteModel(
            name='AgencyName',
        ),
        migrations.DeleteModel(
            name='AgencyType',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='MasterSanctionForm',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
