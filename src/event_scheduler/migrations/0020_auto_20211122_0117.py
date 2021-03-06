# Generated by Django 3.2.7 on 2021-11-22 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0019_auto_20211122_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingitem',
            name='Floor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Floor2', to='event_scheduler.meetingroom', to_field='Floor'),
        ),
        migrations.AlterField(
            model_name='bookingitem',
            name='Room_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Room_number2', to='event_scheduler.meetingroom', to_field='Room_number'),
        ),
    ]
