# Generated by Django 4.1 on 2023-10-09 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_alter_department_department_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='company_name',
            new_name='company',
        ),
    ]
