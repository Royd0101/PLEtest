# Generated by Django 4.1 on 2023-11-22 02:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0024_alter_filelog_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelog',
            name='expired_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]