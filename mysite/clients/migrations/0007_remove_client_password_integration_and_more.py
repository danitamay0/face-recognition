# Generated by Django 5.0 on 2024-07-05 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_alter_client_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='password_integration',
        ),
        migrations.RemoveField(
            model_name='client',
            name='user_integration',
        ),
    ]
