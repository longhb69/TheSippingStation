# Generated by Django 5.0 on 2023-12-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_decorator_price_alter_dlc_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decorator',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='dlc',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True),
        ),
    ]