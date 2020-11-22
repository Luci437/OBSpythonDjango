# Generated by Django 3.0.2 on 2020-04-29 07:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0031_auto_20200424_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticketprize', models.IntegerField(default=0)),
                ('ticketcoin', models.IntegerField(default=0)),
                ('ticketname', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='gameplayed',
            name='startedgame',
            field=models.DateField(default=datetime.datetime(2020, 4, 29, 12, 59, 38, 477348)),
        ),
        migrations.AlterField(
            model_name='gamerating',
            name='reviewtime',
            field=models.DateField(default=datetime.datetime(2020, 4, 29, 12, 59, 38, 476348)),
        ),
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 29, 12, 59, 38, 473347)),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 29, 12, 59, 38, 472346)),
        ),
        migrations.CreateModel(
            name='Lticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticketnumber', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('ticketname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obsapp.TicketType')),
            ],
        ),
    ]
