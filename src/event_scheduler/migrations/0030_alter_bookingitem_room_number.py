# Generated by Django 3.2.7 on 2021-12-04 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0029_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingitem',
            name='Room_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Room', to='event_scheduler.meetingroom', to_field='Room_number'),
        ),
    ]
