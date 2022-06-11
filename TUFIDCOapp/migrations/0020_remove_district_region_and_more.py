# Generated by Django 4.0 on 2022-01-01 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0019_mastersanctionform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='Region',
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
            model_name='mastersanctionform',
            name='Scheme',
        ),
        migrations.RemoveField(
            model_name='region',
            name='AgencyType',
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
        migrations.DeleteModel(
            name='Scheme',
        ),
    ]
