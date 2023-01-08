# Generated by Django 4.1 on 2022-12-12 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning_app', '0005_family_slave'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='family',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='familys_rooms', to='cleaning_app.family'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slave',
            name='family',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='familys_slaves', to='cleaning_app.family'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chore',
            name='slave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cleaning_app.slave'),
        ),
    ]