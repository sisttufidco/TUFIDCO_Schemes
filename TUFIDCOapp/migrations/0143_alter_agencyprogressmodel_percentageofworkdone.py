# Generated by Django 4.0.3 on 2022-03-11 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0142_alter_agencyprogressmodel_valueofworkdone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyprogressmodel',
            name='percentageofworkdone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Percentage of work done'),
        ),
    ]
