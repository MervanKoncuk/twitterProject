# Generated by Django 5.0.2 on 2024-03-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_alter_notificate_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificate',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='İşlem Mesajı'),
        ),
    ]
