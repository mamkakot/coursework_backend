# Generated by Django 4.1 on 2023-01-07 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning_app', '0013_invite_is_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slave',
            name='family',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='familys_slaves', to='cleaning_app.family'),
        ),
    ]