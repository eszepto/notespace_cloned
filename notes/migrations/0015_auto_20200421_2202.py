# Generated by Django 3.0.1 on 2020-04-21 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0014_auto_20200227_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='mean_score',
        ),
        migrations.RemoveField(
            model_name='note',
            name='review_count',
        ),
    ]
