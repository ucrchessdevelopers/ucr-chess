# Generated by Django 3.0.2 on 2020-04-20 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0021_auto_20200419_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_active',
            field=models.DateField(blank=True),
        ),
    ]
