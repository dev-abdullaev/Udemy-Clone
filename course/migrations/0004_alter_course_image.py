# Generated by Django 4.0.3 on 2022-03-20 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_course_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, upload_to='course_images/'),
        ),
    ]