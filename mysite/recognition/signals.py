# recognition/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Face, FaceTraining
import face_recognition
from PIL import Image
import numpy as np

@receiver(post_save, sender=FaceTraining)
def generate_face_encoding(sender, instance, **kwargs):
    if not instance.face_encoding:  # Solo generar si no existe ya una codificación
        print("here")
        #image = face_recognition.load_image_file(instance.image.path)
        #print("facing", image)
        pil_image = Image.open(instance.image.path)
        pil_image = pil_image.convert('RGB')  # Convertir a RGB
        new_image = np.array(pil_image)  # Convertir a array de NumPy

         # Verificar el formato de la imagen
        if new_image.dtype != np.uint8:
                raise ValueError(f"Imagen convertida tiene un tipo no soportado: {new_image.dtype}")
        if len(new_image.shape) != 3 or new_image.shape[2] != 3:
                raise ValueError(f"Imagen convertida tiene un formato no soportado: {new_image.shape}")
        face_encodings = face_recognition.face_encodings(new_image)

        print("face_encodings")
        if face_encodings:
            face_encoding = face_encodings[0]
            instance.face_encoding = ','.join([str(val) for val in face_encoding])
            instance.save()
""" 

def face_generation(image):
        
         """
        