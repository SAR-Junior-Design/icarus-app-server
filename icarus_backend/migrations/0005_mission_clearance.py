# Generated by Django 2.1 on 2018-08-12 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icarus_backend', '0004_clearance'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='clearance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='icarus_backend.Clearance'),
        ),
    ]
