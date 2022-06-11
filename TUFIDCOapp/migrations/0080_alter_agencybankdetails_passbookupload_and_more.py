# Generated by Django 4.0 on 2022-01-15 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUFIDCOapp', '0079_alter_agencysanctionmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencybankdetails',
            name='passbookupload',
            field=models.FileField(help_text='Please attach a clear scanned copy front page of the Bank passbook', null=True, upload_to='passbook/', verbose_name='Passbook Front Page Photo'),
        ),
        migrations.DeleteModel(
            name='AgencySanctionModel',
        ),
    ]
