# Generated by Django 2.1 on 2018-08-23 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icarus_backend', '0016_auto_20180823_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clearance',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
