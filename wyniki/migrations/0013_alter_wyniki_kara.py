# Generated by Django 3.2.9 on 2022-01-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wyniki', '0012_auto_20220106_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wyniki',
            name='kara',
            field=models.CharField(blank=True, choices=[('DNF', 'DNF'), ('DNS', 'DNS'), ('DSQ', 'DSQ'), ('PK', 'PK')], max_length=10, null=True),
        ),
    ]