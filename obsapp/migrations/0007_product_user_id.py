# Generated by Django 3.0.2 on 2020-03-04 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obsapp', '0006_returns'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_id',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='obsapp.LoginTable'),
        ),
    ]