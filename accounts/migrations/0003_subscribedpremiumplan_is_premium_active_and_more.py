# Generated by Django 4.1.4 on 2023-07-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_validity_premiumplan_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribedpremiumplan',
            name='is_Premium_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subscribedpremiumplan',
            name='end_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]