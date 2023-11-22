# Generated by Django 4.1 on 2023-11-22 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0018_alter_file_document_document_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelog',
            name='expiry_date',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expired_date', to='files.file_document'),
        ),
    ]
