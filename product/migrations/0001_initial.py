# Generated by Django 3.1.7 on 2021-06-02 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('variant', models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=10)),
                ('name_supplier', models.CharField(max_length=255)),
                ('phone_supplier', models.CharField(max_length=255)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.categorychild')),
            ],
            options={
                'db_table': 'product_product',
            },
        ),
    ]
