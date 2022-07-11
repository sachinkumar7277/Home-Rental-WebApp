# Generated by Django 3.1.2 on 2021-07-20 06:49

import accounts.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format +919999999999. Up to 10 digits allowed.', regex='^\\+?1?\\d{9,10}$')], verbose_name='Phone')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=100)),
                ('date_of_join', models.DateTimeField(auto_now_add=True)),
                ('date_of_birth', models.DateField()),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageFieldUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to=accounts.models.upload_to, verbose_name='Avatar')),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,10}$')], verbose_name='phone')),
                ('otp', models.CharField(blank=True, max_length=5, null=True)),
                ('Sent_time', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(blank=True, help_text='Number of OTP sent', null=True)),
                ('validated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fullname', models.CharField(blank=True, max_length=100, null=True)),
                ('Email', models.EmailField(max_length=100, null=True, unique=True)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField(null=True)),
                ('pin_no', models.IntegerField(null=True)),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^0?[5-9]{1}\\d{9}$')])),
                ('Profile_pic', models.ImageField(blank=True, max_length=255, null=True, upload_to='Profilepic')),
                ('Premium', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]