# Generated by Django 2.2.1 on 2019-05-16 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmeetingtime',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='groupmeetingtime',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]