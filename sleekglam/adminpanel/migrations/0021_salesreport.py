# Generated by Django 4.0.6 on 2022-10-07 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0020_alter_cat_offer_valid_from_alter_cat_offer_valid_to_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('categoryName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('productPrice', models.FloatField()),
            ],
        ),
    ]
