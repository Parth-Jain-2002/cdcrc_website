# Generated by Django 3.0.7 on 2020-06-11 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('branch', models.CharField(max_length=30)),
                ('course', models.CharField(max_length=10)),
                ('year', models.IntegerField(default=3)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
    ]
