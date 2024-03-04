# Generated by Django 5.0.2 on 2024-02-22 17:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_id_alter_post_save'),
        ('user', '0010_alter_profile_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='save',
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.UUID('ae5a9ceb-cc18-451e-9f08-7907f691de3f'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='likes', to='user.profile', verbose_name='Beğenenler'),
        ),
    ]
