# Generated by Django 3.1.6 on 2021-07-18 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compare', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchs',
            old_name='SearchId',
            new_name='searchId',
        ),
        migrations.RenameField(
            model_name='searchs',
            old_name='SearchName',
            new_name='searchName',
        ),
    ]
