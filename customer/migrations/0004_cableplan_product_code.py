# Generated by Django 4.2.3 on 2023-12-23 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_plan_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cableplan',
            name='product_code',
            field=models.CharField(default='MSCODE', max_length=49),
            preserve_default=False,
        ),
    ]
