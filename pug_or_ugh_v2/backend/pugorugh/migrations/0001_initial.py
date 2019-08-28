# Generated by Django 2.2.4 on 2019-08-28 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image_filename', models.TextField()),
                ('breed', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('gender', multiselectfield.db.fields.MultiSelectField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], default='u', max_length=1)),
                ('size', multiselectfield.db.fields.MultiSelectField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], default='u', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', multiselectfield.db.fields.MultiSelectField(choices=[('b', 'baby'), ('y', 'young'), ('a', 'adult'), ('s', 'senior')], max_length=7)),
                ('gender', multiselectfield.db.fields.MultiSelectField(choices=[('m', 'male'), ('f', 'female'), ('u', 'unknown')], max_length=5)),
                ('size', multiselectfield.db.fields.MultiSelectField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large'), ('u', 'unknown')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', multiselectfield.db.fields.MultiSelectField(choices=[('l', 'liked'), ('d', 'disliked')], max_length=1)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pugorugh.Dog')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
