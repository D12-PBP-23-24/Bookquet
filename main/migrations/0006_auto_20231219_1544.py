# Generated by Django 4.2.4 on 2023-12-19 08:44

from django.db import migrations
from django.core.management import call_command

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_book_isbn'),
    ]

    def load_my_initial_data(apps, schema_editor):
        call_command("loaddata", "main/fixtures/books.json")

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]
