# Generated by Django 5.0.6 on 2024-06-03 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sns_app', '0002_friendrequests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequests',
            old_name='requested_id',
            new_name='requested',
        ),
        migrations.RenameField(
            model_name='friendrequests',
            old_name='sender_id',
            new_name='sender',
        ),
    ]
