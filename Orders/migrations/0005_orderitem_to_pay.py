# Generated by Django 3.2.9 on 2022-06-28 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0004_auto_20220628_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='to_pay',
            field=models.FloatField(default=0),
        ),
    ]