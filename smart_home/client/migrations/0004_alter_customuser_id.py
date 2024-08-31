# Generated by Django 4.2.8 on 2024-01-07 10:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_customuser_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
