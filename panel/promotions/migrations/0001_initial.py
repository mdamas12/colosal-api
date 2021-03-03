# Generated by Django 2.0.5 on 2021-02-12 16:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('products', '0007_auto_20210208_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.FileField(upload_to='uploads')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19)),
                ('coin', models.CharField(choices=[('USD', 'USD'), ('BS', 'BS')], default='USD', max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='categories.Category')),
            ],
            options={
                'verbose_name': 'Promocion',
                'verbose_name_plural': 'Promociones',
            },
        ),
        migrations.CreateModel(
            name='PromotionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
                ('promotion', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='promotion_detail', to='promotions.Promotion')),
            ],
            options={
                'verbose_name': 'Detalle de promocion',
                'verbose_name_plural': 'Detalles de promociones',
            },
        ),
    ]
