# Generated by Django 5.0.7 on 2024-08-02 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_job_detail_farmer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_detail',
            name='posted_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 19, 32, 870596, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='land_detail',
            name='posted_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 19, 32, 871596, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sale_land',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 19, 32, 872596, tzinfo=datetime.timezone.utc)),
        ),
    ]