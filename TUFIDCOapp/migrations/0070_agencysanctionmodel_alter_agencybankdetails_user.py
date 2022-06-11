# Generated by Django 4.0 on 2022-01-11 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('TUFIDCOapp', '0069_agencybankdetails_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencySanctionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Latitude', models.IntegerField(null=True, verbose_name='Latitude')),
            ],
        ),
        migrations.AlterField(
            model_name='agencybankdetails',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
