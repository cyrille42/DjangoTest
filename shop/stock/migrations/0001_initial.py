# Generated by Django 4.0.3 on 2022-03-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_description', models.CharField(max_length=200)),
                ('categorie', models.CharField(choices=[(1, 'nouriture'), (2, 'éléctronique'), (3, 'épicerie'), (4, 'hygiéne')], max_length=32)),
                ('price', models.IntegerField()),
                ('product_number', models.IntegerField()),
                ('discount', models.IntegerField(default=0)),
                ('special_discount', models.IntegerField(default=1)),
                ('special_discount_gift', models.IntegerField(default=1)),
            ],
        ),
    ]