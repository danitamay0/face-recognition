# ViewSets define the view behavior.

import requests
from mysite.settings import DOMAIN, MEDIA_ROOT

from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import os
import face_recognition

from mysite.settings import MEDIA_ROOT
from recognition.models import Face, FaceTraining

from django.core.files import File
from sklearn.model_selection import train_test_split
import numpy as np

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def charge_faces_test(request):
    try:
        client_id = request.auth.get('client')
       
       
        dir_ = os.path.join(MEDIA_ROOT, f"training_humans/")
        pix = os.listdir(dir_)
        pos = int(request.data['pos'])
        newarr = np.array_split(pix, 20) # len 14 pos 13
        print(pos, len(newarr[pos]), newarr[pos])
        
        for person in newarr[pos]:
            name = person.replace(".jpg", " TRAINING")
            name = name.replace(".png", " TRAINING")
            name = name.replace(".jpeg", " TRAINING")
            image_path = os.path.join(dir_, person)
            print(f"sending: {image_path=}")
            if not os.path.isfile(image_path):
                print("is not file: ", image_path)
                continue
            headers = {"Authorization": f"Bearer {request.auth}"}
            r = requests.post(f"{DOMAIN}/faces/charge-face",
                            data={'face': person, 'name': name},
                            headers=headers)
            print(f'{r.text=}')
            
    except Exception as e:
        print("Error", e)
        return Response("Error", 500)
    return Response("Migration successfull")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def charge_face(request):
    try:
        client_id = request.auth.get('client')
        person = request.data['name']
        face_ = request.data['face']
        
        dir_ = os.path.join(MEDIA_ROOT, f"training_humans/")
        unknow_face = os.path.join(dir_, face_)
        if not unknow_face:
            return Response('Es obligatoria la imagen', 400)

        new_image = face_recognition.load_image_file(unknow_face)

        # Obtener las codificaciones faciales de la nueva imagen
        face_encodings = face_recognition.face_encodings(new_image)
    
        if not face_encodings:
            print("No se encontró rostro")
            return Response('No se encontró rostro', 400)

        name = person.replace(".jpg", " TRAINING")
        name = person.replace(".png", " TRAINING")
        name = person.replace(".jpeg", " TRAINING")
        if face_encodings:
            
            face = Face(client_id=client_id, name=name)
            face.save()
               
            with open(unknow_face, 'rb') as img_file:
                    fcds = ','.join([str(val) for val in face_encodings[0]])
                    django_file = File(img_file)
                    FaceTraining(face=face, image=django_file, face_encoding=fcds).save()
    except Exception as e:
        print("Error", e)
        return Response("Error", 500)
    return Response("Migration successfull")
