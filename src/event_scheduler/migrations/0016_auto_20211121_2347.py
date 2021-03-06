# Generated by Django 3.2.7 on 2021-11-22 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0015_auto_20211120_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingitem',
            name='Floor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='floor2floor', to='event_scheduler.meetingroom'),
        ),
        migrations.AlterField(
            model_name='meetingroom',
            name='Floor',
            field=models.CharField(max_length=2),
        ),
    ]
