# Generated by Django 4.1 on 2023-10-09 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_remove_file_document_select_bu_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
