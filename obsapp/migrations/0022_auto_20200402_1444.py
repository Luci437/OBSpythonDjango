# Generated by Django 3.0.2 on 2020-04-02 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0021_auto_20200401_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 2, 14, 44, 15, 666344)),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 2, 14, 44, 15, 665343)),
        ),
    ]
