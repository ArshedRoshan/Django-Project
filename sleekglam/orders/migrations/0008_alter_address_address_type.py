# Generated by Django 4.0.6 on 2022-09-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Address_type',
            field=models.CharField(default='HOME', max_length=50),
        ),
    ]