# Generated by Django 4.1.3 on 2023-01-17 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_category_post_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='auther',
            new_name='author',
        ),
    ]
