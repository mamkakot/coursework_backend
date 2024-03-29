# Generated by Django 4.1 on 2023-01-03 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning_app', '0009_remove_chore_condition_chore_period_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='cleaning_app.slave')),
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='cleaning_app.slave')),
            ],
        ),
    ]
