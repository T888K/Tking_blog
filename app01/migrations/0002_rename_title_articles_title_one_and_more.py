# Generated by Django 4.2 on 2023-04-20 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articles',
            old_name='title',
            new_name='title_one',
        ),
        migrations.RenameField(
            model_name='articles',
            old_name='source',
            new_name='title_three',
        ),
        migrations.RenameField(
            model_name='articles',
            old_name='author',
            new_name='title_two',
        ),
    ]