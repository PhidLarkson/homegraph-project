# Generated by Django 4.2.8 on 2024-02-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_alter_serialconfigurationobjecta_config_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomobjectidentifiers',
            name='config_id',
            field=models.IntegerField(default=8),
        ),
    ]
