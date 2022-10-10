# Generated by Django 4.0.6 on 2022-09-15 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0004_alter_banner_banner_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='is_selected',
        ),
        migrations.AddField(
            model_name='banner',
            name='content1',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='content2',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
