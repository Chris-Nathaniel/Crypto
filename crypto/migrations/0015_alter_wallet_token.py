# Generated by Django 5.1.7 on 2025-04-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0014_transaction_session_id_wallet_session_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='token',
            field=models.CharField(max_length=64),
        ),
    ]
