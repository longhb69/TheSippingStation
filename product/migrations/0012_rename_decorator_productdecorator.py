# Generated by Django 5.0 on 2023-12-14 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_game_storage_min_alter_game_storage_rec'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Decorator',
            new_name='ProductDecorator',
        ),
    ]