# Generated by Django 5.1.2 on 2024-10-23 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_remove_shortenedurl_short_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortenedurl',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]
