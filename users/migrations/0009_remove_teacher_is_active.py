# Generated by Django 4.0.3 on 2022-03-03 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_teacher_email_remove_teacher_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='is_active',
        ),
    ]