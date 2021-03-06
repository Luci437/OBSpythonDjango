# Generated by Django 3.0.2 on 2020-04-22 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0029_auto_20200419_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='highestscore',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gamerating',
            name='reviewtime',
            field=models.DateField(default=datetime.datetime(2020, 4, 22, 21, 10, 44, 224477)),
        ),
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 22, 21, 10, 44, 222475)),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 22, 21, 10, 44, 221475)),
        ),
    ]
