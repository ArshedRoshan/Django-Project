# Generated by Django 4.0.6 on 2022-09-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0002_remove_product_subcategories_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='content',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
