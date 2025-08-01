# Generated by Django 5.1.7 on 2025-04-02 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='quantity',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wallet',
            name='quantity',
            field=models.DecimalField(decimal_places=3, default=2, max_digits=10),
            preserve_default=False,
        ),
    ]
