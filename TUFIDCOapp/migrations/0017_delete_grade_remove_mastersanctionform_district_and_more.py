# Generated by Django 4.0 on 2021-12-31 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0016_remove_mastersanctionform_agencyname_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.RemoveField(
            model_name='mastersanctionform',
            name='District',
        ),
        migrations.RemoveField(
            model_name='mastersanctionform',
            name='Region',
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
