# Generated by Django 5.1.5 on 2025-01-31 09:22

import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('email_notification', models.BooleanField(default=False)),
                ('balance', models.FloatField(default=0.0)),
                ('first_name', models.CharField(max_length=99)),
                ('middle_name', models.CharField(max_length=99)),
                ('last_name', models.CharField(max_length=99)),
                ('area_code', models.CharField(default='+234', max_length=4)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=249)),
                ('user_ID', models.CharField(blank=True, db_index=True, max_length=11, null=True, unique=True)),
                ('pin', models.CharField(blank=True, max_length=4, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(db_index=True, max_length=10, unique=True)),
                ('account_name', models.CharField(db_index=True, max_length=299)),
                ('txn_limit', models.FloatField(default=100000)),
                ('picture', models.ImageField(upload_to='img/')),
                ('account_type', models.CharField(choices=[('Savings', 'Savings'), ('Current', 'Current')], max_length=10)),
                ('bvn', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField()),
                ('street_address', models.CharField(max_length=99)),
                ('city', models.CharField(max_length=99)),
                ('state', models.CharField(choices=[('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara'), ('FCT', 'FCT')], max_length=99)),
                ('zip', models.CharField(max_length=9)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('marital_status', models.CharField(choices=[('Married', 'Married'), ('Single', 'Single'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Separated', 'Separated')], max_length=10)),
                ('occupation', models.CharField(max_length=99)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=299)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(db_index=True, max_length=299)),
                ('picture', models.ImageField(upload_to='img/')),
                ('date_of_birth', models.DateField()),
                ('street_address', models.CharField(max_length=99)),
                ('city', models.CharField(max_length=99)),
                ('state', models.CharField(choices=[('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara'), ('FCT', 'FCT')], max_length=99)),
                ('zip', models.CharField(max_length=9)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('marital_status', models.CharField(choices=[('Married', 'Married'), ('Single', 'Single'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed'), ('Separated', 'Separated')], max_length=10)),
                ('occupation', models.CharField(max_length=99)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
