# Generated by Django 3.2.7 on 2021-11-24 04:53

from django.db import migrations, models
import event_scheduler.utils


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0024_auto_20211123_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingitem',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
