# Generated by Django 5.0.2 on 2024-02-22 17:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('a0e71c0a-8d5a-41f7-a35c-d328ed83361f'), editable=False, primary_key=True, serialize=False),
        ),
    ]
