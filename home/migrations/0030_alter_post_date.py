# Generated by Django 5.0.7 on 2024-07-29 19:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 7, 29, 19, 23, 51, 83902)),
        ),
    ]