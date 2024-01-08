# Generated by Django 4.1 on 2024-01-08 00:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import receipt.models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0035_person_document_company'),
        ('receipt', '0003_receipt_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person_Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fined', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('receipt', models.FileField(blank=True, null=True, upload_to=receipt.models.get_upload_path)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('person_document', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='files.person_document')),
            ],
        ),
    ]