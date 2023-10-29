from django.db import migrations
from django.core.management import call_command

def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "main/fixtures/books.json")

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20231029_2323'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]