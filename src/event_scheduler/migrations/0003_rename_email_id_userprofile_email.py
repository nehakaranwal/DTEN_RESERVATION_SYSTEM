# Generated by Django 3.2.7 on 2021-11-08 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0002_userprofile_is_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='email_id',
            new_name='email',
        ),
    ]
