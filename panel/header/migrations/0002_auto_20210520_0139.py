# Generated by Django 2.0.5 on 2021-05-20 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('header', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='action_link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='slide',
            name='action_title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='slide',
            name='span',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='slide',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
