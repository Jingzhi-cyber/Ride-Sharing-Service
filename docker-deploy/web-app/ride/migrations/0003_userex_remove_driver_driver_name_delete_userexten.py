# Generated by Django 4.1.5 on 2023-02-04 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ride', '0002_alter_ride_destination_vehicle_userexten_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_driver', models.CharField(choices=[('false', 'false'), ('true', 'true')], default='false', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='driver',
            name='driver_name',
        ),
        migrations.DeleteModel(
            name='UserExten',
        ),
    ]
