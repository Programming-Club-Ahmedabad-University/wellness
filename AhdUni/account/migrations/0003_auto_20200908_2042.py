# Generated by Django 3.0.8 on 2020-09-08 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200905_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='daily_water',
            field=models.IntegerField(),
        ),
    ]
