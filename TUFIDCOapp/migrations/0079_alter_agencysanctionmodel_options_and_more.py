# Generated by Django 4.0 on 2022-01-15 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0078_alter_agencysanctionmodel_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencysanctionmodel',
            options={'verbose_name': 'Agency Progress Detail', 'verbose_name_plural': 'Agency Progress Details'},
        ),
        migrations.AddField(
            model_name='agencysanctionmodel',
            name='valueofworkdone',
            field=models.CharField(max_length=50, null=True, verbose_name='Value of Work done'),
        ),
    ]
