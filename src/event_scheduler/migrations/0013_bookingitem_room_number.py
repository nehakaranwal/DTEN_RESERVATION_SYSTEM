# Generated by Django 3.2.7 on 2021-11-20 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0012_auto_20211119_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingitem',
            name='Room_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event_scheduler.meetingroom'),
        ),
    ]
