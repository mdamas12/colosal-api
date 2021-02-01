# Generated by Django 2.0.5 on 2021-01-18 15:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210118_0201'),
        ('categories', '0001_initial'),
        ('combos', '0003_auto_20210118_0224'),
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
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='combos.Promotion')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product')),
            ],
            options={
                'verbose_name': 'Detalle de promocion',
                'verbose_name_plural': 'Detalles de promociones',
            },
        ),
        migrations.RemoveField(
            model_name='combo',
            name='category',
        ),
        migrations.RemoveField(
            model_name='combodetail',
            name='combo',
        ),
        migrations.RemoveField(
            model_name='combodetail',
            name='product',
        ),
        migrations.DeleteModel(
            name='Combo',
        ),
        migrations.DeleteModel(
            name='ComboDetail',
        ),
    ]
