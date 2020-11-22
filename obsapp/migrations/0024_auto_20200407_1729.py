# Generated by Django 3.0.2 on 2020-04-07 11:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0023_auto_20200404_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2000)),
                ('option1', models.CharField(max_length=500)),
                ('option2', models.CharField(max_length=500)),
                ('option3', models.CharField(max_length=500)),
                ('option4', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 7, 17, 29, 32, 631592)),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 7, 17, 29, 32, 630592)),
        ),
    ]