# ViewSets define the view behavior.

from mysite.settings import MEDIA_ROOT

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import os
import face_recognition

from mysite.settings import MEDIA_ROOT
from recognition.models import Face, FaceTraining

from django.core.files import File

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def charge_faces_test(request):
    try:
        client_id = request.auth.get('client')
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
                print("No se encontró rostro")
                continue

            name = person.replace(".jpg", " TRAINING")
            name = person.replace(".png", " TRAINING")
            name = person.replace(".jpeg", " TRAINING")
            if face_encodings:
                
                face = Face(client= client_id, name=name )
                face.save()
                
                with open(image_path, 'rb') as img_file:
                    fcds = ','.join([str(val) for val in face_encodings[0]])
                    django_file = File(img_file)
                    FaceTraining(face=face, image=django_file, face_encoding=fcds).save()
    except Exception as e:
        print("Error", e)
        return Response("Error", 500)
    return Response("Migration successfull")
