# Generated by Django 3.0.2 on 2020-03-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0014_product_lcoin'),
    ]

    operations = [
        migrations.AddField(
            model_name='logintable',
            name='lcoin',
            field=models.IntegerField(default=100),
        ),
    ]
