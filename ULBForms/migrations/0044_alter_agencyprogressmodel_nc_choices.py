# Generated by Django 4.0.4 on 2022-05-22 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULBForms', '0043_alter_agencyprogressmodel_expenditure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyprogressmodel',
            name='nc_choices',
            field=models.CharField(choices=[('TS to be obtained', 'TS to be obtained'), ('Tender Stage', 'Tender Stage'), ('Work Order to be Issued', 'Work Order to be Issued'), ('Others', 'Others')], help_text='Select/Tick any one of the about if status is TO BE COMMENCED', max_length=30, null=True, verbose_name='If To be Commenced'),
        ),
    ]
