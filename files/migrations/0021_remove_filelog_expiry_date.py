# Generated by Django 4.1 on 2023-11-22 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0020_alter_filelog_expiry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filelog',
            name='expiry_date',
        ),
    ]
