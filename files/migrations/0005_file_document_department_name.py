# Generated by Django 4.1 on 2023-10-09 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_rename_company_name_department_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_document',
            name='department_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.department'),
        ),
    ]
