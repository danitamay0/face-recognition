# Generated by Django 5.0 on 2024-07-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='face_encoding',
            field=models.TextField(blank=True),
        ),
    ]
