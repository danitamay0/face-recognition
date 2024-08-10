from django.core.management.base import BaseCommand
import os
import face_recognition

from clients.models import Client
from mysite.settings import MEDIA_URL, MEDIA_ROOT
from recognition.models import Face, FaceTraining
from PIL import Image
import numpy as np
from django.core.files import File

class Command(BaseCommand):
    # python3 manage.py help welcome
    help = 'Create faces by command'  
  
    def add_arguments(self, parser):
        parser.add_argument('client_id',  help='Client ID')
        
    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
        dir_ = os.path.join(MEDIA_ROOT, f"training_humans/")
        pix = os.listdir(dir_)
        print(f"{pix=}")
        print(f"{client_id=}")
    
        for person in pix:
            
            image_path = os.path.join(dir_, person)
            if not os.path.isfile(image_path):
                continue

            new_image = face_recognition.load_image_file(image_path)

            # Obtener las codificaciones faciales de la nueva imagen
            face_encodings = face_recognition.face_encodings(new_image)
            print(f"{image_path=}")

            if not face_encodings:
                self.stdout.write("No se encontró ninguna cara en la imagen")
                continue

            name = person.replace(".jpg", " TRAINING")
            if face_encodings:
                client = Client.objects.get(id = client_id)
                
                face = Face(client= client, name=name )
                face.save()
                
                with open(image_path, 'rb') as img_file:
                    fcds = ','.join([str(val) for val in face_encodings[0]])
                    django_file = File(img_file)
                    FaceTraining(face=face, image=django_file, face_encoding=fcds).save()
                    
        self.stdout.write("Models Createds")