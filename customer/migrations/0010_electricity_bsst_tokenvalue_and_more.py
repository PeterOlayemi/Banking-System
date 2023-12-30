# Generated by Django 4.2.3 on 2023-12-27 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_electricity_electricityservice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='electricity',
            name='bsst_tokenvalue',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='customer_reference',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='exchange_reference',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='receipt_number',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='standard_tokenvalue',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='token',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='unit',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
        migrations.AddField(
            model_name='electricity',
            name='utility_name',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
    ]