# Generated by Django 4.1 on 2023-11-20 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0017_filelog_previous_file_alter_filelog_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_document',
            name='document_type',
            field=models.CharField(max_length=50),
        ),
    ]