# Generated by Django 4.2.7 on 2023-11-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_blusainstance_blusa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='talla',
            field=models.CharField(blank=True, help_text='Agregue la talla de la prenda.', max_length=100, null=True),
        ),
    ]
