# Generated by Django 2.0.7 on 2018-08-22 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icarus_backend', '0011_auto_20180822_0201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drone',
            old_name='drone_type',
            new_name='type',
        ),
    ]
