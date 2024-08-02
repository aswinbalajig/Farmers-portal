# Generated by Django 5.0.7 on 2024-08-02 15:19

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_job_detail_posted_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_detail',
            name='farmer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.register_detail'),
        ),
        migrations.AlterField(
            model_name='job_detail',
            name='posted_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 19, 19, 412252, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='land_detail',
            name='posted_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 19, 19, 412252, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sale_land',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 8, 2, 15, 19, 19, 413252, tzinfo=datetime.timezone.utc)),
        ),
    ]