# Generated by Django 3.2.6 on 2022-07-06 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trial', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='client_id',
        ),
    ]
