# Generated by Django 5.0.2 on 2024-02-22 17:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('e1537588-5742-4639-bc3a-b2e3a40d47df'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
