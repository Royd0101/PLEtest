# Generated by Django 4.1 on 2023-11-22 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0029_filelog_expired_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filelog',
            name='expired_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
