# Generated by Django 4.0.3 on 2022-03-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='learning_goal',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]