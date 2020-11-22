# Generated by Django 3.0.2 on 2020-04-04 16:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0022_auto_20200402_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_editable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 22, 5, 16, 872785)),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 22, 5, 16, 871785)),
        ),
    ]