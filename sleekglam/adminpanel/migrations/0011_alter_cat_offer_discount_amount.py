# Generated by Django 4.0.6 on 2022-09-25 12:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0010_cat_offer_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat_offer',
            name='discount_amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]