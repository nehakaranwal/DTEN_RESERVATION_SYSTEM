# Generated by Django 3.2.7 on 2021-11-16 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0007_rename_is_staff_userprofile_is_vaccinated'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
