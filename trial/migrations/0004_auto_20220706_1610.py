# Generated by Django 3.2.6 on 2022-07-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trial', '0003_auto_20220706_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='Invoiceitems',
        ),
        migrations.AddField(
            model_name='invoice',
            name='Invoiceitems',
            field=models.ManyToManyField(to='trial.items'),
        ),
    ]