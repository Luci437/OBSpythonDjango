# Generated by Django 3.0.2 on 2020-03-19 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0011_ads_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='about_user',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
