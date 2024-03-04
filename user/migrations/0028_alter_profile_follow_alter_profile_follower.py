# Generated by Django 5.0.2 on 2024-02-26 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='takip', to='user.profile', verbose_name='Takip edilenler'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='takipci', to='user.profile', verbose_name='Takipçiler'),
        ),
    ]
