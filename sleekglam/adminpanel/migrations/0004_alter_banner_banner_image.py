# Generated by Django 4.0.6 on 2022-09-15 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0003_banner_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_image',
            field=models.ImageField(blank=True, upload_to='static'),
        ),
    ]
