# Generated by Django 4.1 on 2022-12-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning_app', '0007_room_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='date done'),
        ),
    ]
