# Generated by Django 4.1 on 2023-01-19 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cleaning_app', '0014_alter_slave_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='slave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]