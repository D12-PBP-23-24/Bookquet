# Generated by Django 4.2.4 on 2023-10-29 07:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0016_remove_book_favorited_by_book_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_books', to=settings.AUTH_USER_MODEL),
        ),
    ]