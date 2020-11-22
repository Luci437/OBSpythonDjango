# Generated by Django 3.0.2 on 2020-04-18 18:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0028_auto_20200418_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationz',
            name='notificationtime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 19, 0, 6, 3, 704967)),
        ),
        migrations.AlterField(
            model_name='questions',
            name='typeofqst',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='requestexchange',
            name='datetimeofrequest',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 19, 0, 6, 3, 702965)),
        ),
        migrations.CreateModel(
            name='GameRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=2000)),
                ('reviewtime', models.DateField(default=datetime.datetime(2020, 4, 19, 0, 6, 3, 709970))),
                ('gameid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obsapp.Games')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obsapp.UserInformation')),
            ],
        ),
    ]