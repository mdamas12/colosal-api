# Generated by Django 2.0.5 on 2021-03-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(null=True, upload_to='uploads'),
        ),
    ]
