# Generated by Django 2.2.8 on 2020-08-31 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200808_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_graph_workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_time', models.IntegerField()),
                ('workout_date', models.DateField()),
            ],
        ),
    ]
