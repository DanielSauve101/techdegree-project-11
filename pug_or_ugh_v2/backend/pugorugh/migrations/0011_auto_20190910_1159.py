# Generated by Django 2.2.4 on 2019-09-10 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0010_auto_20190906_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
