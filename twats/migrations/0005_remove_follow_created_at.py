# Generated by Django 3.0.3 on 2020-06-01 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twats', '0004_auto_20200601_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='created_at',
        ),
    ]
