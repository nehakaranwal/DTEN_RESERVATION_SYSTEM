# Generated by Django 3.2.7 on 2021-11-24 17:35

from django.db import migrations, models
import event_scheduler.utils


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0025_auto_20211123_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='name',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='bookingitem',
            name='Booking_id',
            field=models.CharField(default=event_scheduler.utils.create_new_ref_number, max_length=10, unique=True),
        ),
    ]
