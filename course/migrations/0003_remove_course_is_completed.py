# Generated by Django 4.0.3 on 2022-03-09 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='is_completed',
        ),
    ]