# Generated by Django 3.1.2 on 2020-11-02 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20201030_2137'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('product', 'size', 'quantity')},
        ),
    ]
