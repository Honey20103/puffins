# Generated by Django 3.1.2 on 2020-10-25 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20201023_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]