# Generated by Django 3.2.7 on 2021-11-07 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import event_scheduler.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email_id', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookingItem',
            fields=[
                ('Booking_id', models.CharField(blank=True, default=event_scheduler.utils.create_new_ref_number, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('Business_unit', models.CharField(choices=[('IT', 'Information Technology'), ('HR', 'Human_Resource'), ('FIN', 'Finance'), ('MK', 'Marketing'), ('DG', 'Digital')], default='IT', max_length=3)),
                ('Floor', models.CharField(max_length=255)),
                ('Date', models.DateTimeField(verbose_name='Date')),
                ('User_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
