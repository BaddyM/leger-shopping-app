# Generated by Django 4.2.8 on 2024-04-10 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legerapp', '0002_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(null=True, upload_to='product_images'),
        ),
    ]
