# Generated by Django 3.0.2 on 2020-04-20 03:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0015_auto_20200419_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_active',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 4, 19, 20, 21, 40, 940378)),
        ),
    ]