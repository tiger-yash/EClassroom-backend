# Generated by Django 3.2.6 on 2021-08-29 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_auto_20210829_0127'),
        ('authentication', '0002_googleauth'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='classes',
            field=models.ManyToManyField(blank=True, related_name='classes', to='classes.Classes'),
        ),
    ]
