# Generated by Django 3.0.14 on 2021-05-22 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0015_auto_20210522_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceimage',
            name='image',
            field=models.ImageField(upload_to='resources/images/29753252/'),
        ),
    ]
