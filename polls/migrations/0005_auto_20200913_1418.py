# Generated by Django 3.1.1 on 2020-09-13 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200913_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='body',
            new_name='body_text',
        ),
    ]
