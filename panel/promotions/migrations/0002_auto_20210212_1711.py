# Generated by Django 2.0.5 on 2021-02-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='status',
            field=models.CharField(default='ACTIVE', max_length=20),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='image',
            field=models.FileField(null=True, upload_to='uploads'),
        ),
    ]
