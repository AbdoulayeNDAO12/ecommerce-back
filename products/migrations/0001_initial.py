# Generated by Django 3.1.6 on 2021-07-18 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=2552)),
                ('more_info', models.TextField()),
                ('price', models.IntegerField()),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('category', models.ManyToManyField(related_name='products', to='categories.Category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
