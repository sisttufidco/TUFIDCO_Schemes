# Generated by Django 4.0 on 2022-01-02 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0024_alter_postmainslider_mainsliders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastersanctionform',
            name='Project_ID',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Project ID'),
        ),
    ]
