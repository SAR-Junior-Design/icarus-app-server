# Generated by Django 2.0.7 on 2018-07-26 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('mission_id', models.TextField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('type', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('starts_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField()),
            ],
        ),
    ]
