# Generated by Django 3.0.4 on 2020-04-18 12:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0008_auto_20200418_0846'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Userdata',
        ),
    ]
