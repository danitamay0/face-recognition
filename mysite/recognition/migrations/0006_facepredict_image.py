# Generated by Django 5.0 on 2024-08-10 16:59

import recognition.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recognition", "0005_rename_client_id_facepredict_client_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="facepredict",
            name="image",
            field=models.ImageField(
                null=True,
                upload_to=recognition.models.face_predict_path,
                verbose_name="Imagen",
            ),
        ),
    ]
