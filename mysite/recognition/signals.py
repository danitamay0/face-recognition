# recognition/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Face
import face_recognition

@receiver(post_save, sender=Face)
def generate_face_encoding(sender, instance, **kwargs):
    if not instance.face_encoding:  # Solo generar si no existe ya una codificación
        image = face_recognition.load_image_file(instance.image.path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            face_encoding = face_encodings[0]
            instance.face_encoding = ','.join([str(val) for val in face_encoding])
            instance.save()
