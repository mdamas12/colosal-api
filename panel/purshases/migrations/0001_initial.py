# Generated by Django 2.0.5 on 2021-01-20 14:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('providers', '0001_initial'),
        ('products', '0005_auto_20210118_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('invoice', models.TextField(blank=True, null=True)),
                ('coin', models.CharField(choices=[('USD', 'USD'), ('BS', 'BS')], default='USD', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('porvider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='providers.Provider')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=19)),
                ('purchase_quantity', models.IntegerField(default=0)),
                ('purchase_Received', models.IntegerField(default=0)),
                ('status', models.CharField(default='Incomplete', max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='purshases.Purchase')),
            ],
            options={
                'verbose_name': 'Detalle de producto',
                'verbose_name_plural': 'Detalles de productos',
            },
        ),
    ]
