# Generated by Django 5.0.4 on 2024-04-11 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legerapp', '0003_alter_product_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(null=True, upload_to='product_images/'),
        ),
    ]
