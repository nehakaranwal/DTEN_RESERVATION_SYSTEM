# Generated by Django 3.2.7 on 2021-11-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0014_auto_20211120_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingitem',
            name='status',
        ),
        migrations.AlterField(
            model_name='bookingitem',
            name='time_id',
            field=models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '13:00'), (7, '14:00'), (8, '15:00'), (9, '16:00'), (10, '17:00'), (11, '18:00'), (12, '19:00'), (13, '20:00')]),
        ),
    ]
