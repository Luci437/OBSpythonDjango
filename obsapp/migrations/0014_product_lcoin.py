# Generated by Django 3.0.2 on 2020-03-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0013_auto_20200319_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='lcoin',
            field=models.IntegerField(default=0),
        ),
    ]
