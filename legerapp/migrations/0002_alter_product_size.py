# Generated by Django 4.2.8 on 2024-04-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=100),
        ),
    ]
