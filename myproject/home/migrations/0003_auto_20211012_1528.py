# Generated by Django 3.2.7 on 2021-10-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooditem',
            name='Quantity',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='description',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
