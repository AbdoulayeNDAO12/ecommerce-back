# Generated by Django 3.1.6 on 2021-07-17 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Searchs',
            fields=[
                ('SearchId', models.AutoField(primary_key=True, serialize=False)),
                ('SearchName', models.CharField(max_length=100)),
            ],
        ),
    ]
