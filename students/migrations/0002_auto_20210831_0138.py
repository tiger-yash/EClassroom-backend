# Generated by Django 3.2.6 on 2021-08-31 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentssubmission',
            name='marks',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3),
        ),
        migrations.AddField(
            model_name='testssubmission',
            name='marks',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3),
        ),
    ]
