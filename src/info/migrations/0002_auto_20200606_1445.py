# Generated by Django 3.0.5 on 2020-06-06 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='created',
        ),
        migrations.RemoveField(
            model_name='news',
            name='created',
        ),
        migrations.AddField(
            model_name='events',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='events',
            name='venue',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
