# Generated by Django 5.0.7 on 2024-08-22 00:55

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('it_users', '0003_profile_bio_profile_realname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=85, scale=None, size=[600, 600], upload_to='avatars/'),
        ),
    ]
