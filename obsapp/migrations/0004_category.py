# Generated by Django 3.0.2 on 2020-03-04 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0003_auto_20200220_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=100)),
            ],
        ),
    ]
