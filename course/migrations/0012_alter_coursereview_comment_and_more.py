# Generated by Django 4.0.3 on 2022-03-22 09:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_alter_coursereview_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursereview',
            name='comment',
            field=models.TextField(default='No Comment'),
        ),
        migrations.AlterField(
            model_name='coursereview',
            name='stars_given',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]