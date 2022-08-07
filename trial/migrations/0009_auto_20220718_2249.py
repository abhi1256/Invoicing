# Generated by Django 3.2.6 on 2022-07-18 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trial', '0008_auto_20220718_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='billed_by',
            name='City',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_by',
            name='Country',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_by',
            name='Pincode',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_by',
            name='Street',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_to',
            name='City',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_to',
            name='Country',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_to',
            name='Pincode',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='billed_to',
            name='Street',
            field=models.CharField(default='None', max_length=150, null=True),
        ),
    ]
