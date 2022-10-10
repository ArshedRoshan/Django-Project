# Generated by Django 4.0.6 on 2022-09-30 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0019_product_offer_valid_from_product_offer_valid_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat_offer',
            name='valid_from',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='cat_offer',
            name='valid_to',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='product_offer',
            name='valid_from',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='product_offer',
            name='valid_to',
            field=models.DateField(null=True),
        ),
    ]
