# Generated by Django 3.2.7 on 2021-11-22 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_scheduler', '0020_auto_20211122_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingitem',
            name='User_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='User_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
