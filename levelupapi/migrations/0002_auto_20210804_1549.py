# Generated by Django 3.2.6 on 2021-08-04 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='host',
            new_name='organizer',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
    ]
