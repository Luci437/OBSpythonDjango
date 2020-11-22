# Generated by Django 3.0.2 on 2020-04-17 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0026_auto_20200417_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='typeofqst',
            field=models.CharField(choices=[('EASY', 'EASY'), ('MEDIUM', 'MEDIUM'), ('HARD', 'HARD')], default='EASY', max_length=50),
        ),
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 17, 22, 57, 50, 770411)),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 17, 22, 57, 50, 769410)),
        ),
    ]