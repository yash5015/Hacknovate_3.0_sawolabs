# Generated by Django 3.2.7 on 2021-10-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20211012_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooditem',
            name='description',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='Quantity',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
