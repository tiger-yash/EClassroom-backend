# Generated by Django 3.2.6 on 2021-08-31 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_auto_20210829_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='max_marks',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='test',
            name='max_marks',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]