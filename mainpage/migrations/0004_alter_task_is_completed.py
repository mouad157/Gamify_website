# Generated by Django 4.2 on 2023-04-09 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_remove_reveiw_task_image_mark_image_origin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
