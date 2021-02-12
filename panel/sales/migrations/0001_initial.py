# Generated by Django 2.0.5 on 2021-02-08 20:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('payments', '0002_auto_20210204_0009'),
        ('shoppingcart', '0002_auto_20210204_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.TextField(blank=True, null=True)),
                ('payment_type', models.CharField(choices=[('ZELLE', 'ZELLE'), ('TRANSFERENCIA BS', 'TRANSFERENCIA BS'), ('TRANSFERENCIA $PAGO MOVIL', 'TRANSFERENCIA $PAGO MOVIL'), ('EFECTIVO', 'EFECTIVO')], default='TRANSFERENCIA BS', max_length=20)),
                ('coin', models.CharField(choices=[('USD', 'USD'), ('BS', 'BS')], default='USD', max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('status', models.CharField(max_length=10)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payments.Bank')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customers.Customer')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sale_Product', to='shoppingcart.Shoppingcart')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sale_detail', to='sales.Sale')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalles de ventas',
            },
        ),
    ]
