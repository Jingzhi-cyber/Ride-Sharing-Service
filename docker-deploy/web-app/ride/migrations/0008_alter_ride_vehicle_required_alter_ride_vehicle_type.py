# Generated by Django 4.1.5 on 2023-02-08 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0007_ride_vehicle_required_alter_ride_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='vehicle_required',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
