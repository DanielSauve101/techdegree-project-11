# Generated by Django 2.2.4 on 2019-08-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0003_auto_20190829_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='breed',
            field=models.CharField(default='unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], default='u', max_length=1),
        ),
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], default='u', max_length=2),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'liked'), ('d', 'disliked')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(choices=[('b', 'baby'), ('y', 'young'), ('a', 'adult'), ('s', 'senior')], max_length=4),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], max_length=3),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], max_length=6),
        ),
    ]
