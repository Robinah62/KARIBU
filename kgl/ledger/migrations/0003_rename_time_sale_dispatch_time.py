# Generated by Django 5.2 on 2025-04-28 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_alter_creditsale_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='time',
            new_name='dispatch_time',
        ),
    ]
