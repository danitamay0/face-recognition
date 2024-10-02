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
from recognition.ml.knn_recognition import  predict, train

from recognition.models import StatusFace

from sklearn.metrics import confusion_matrix, accuracy_score

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_knn(request):
    print("Training KNN classifier...")
    client = request.auth.get('client')
    TRAIN_DIR = './train_dir/'
    TEST_DIR = './test_dir/'
    people_training = Face.objects.filter(client=client, status=StatusFace.ACT)
    known_faces_path = f"{MEDIA_ROOT}/test_dataset/known_faces"

    model_knn = train(people_training, n_neighbors=3, client_id=client)


    test_dir = os.listdir(known_faces_path)

    X_test = []
    y = []
    y_pred = []


    # Loop through each person in the training directory
    for person in test_dir:
        pix = os.listdir(f"{known_faces_path}/{person}" )

        # Loop through each training image for the current person
        for person_img in pix:

            X_test.append([person,person_img])

            # Get the face encodings for the face in each image file
            path_img = f"{known_faces_path}/{person}/{person_img}"

            predictions = predict(path_img, model_knn)
            print(f"{person=} = {predictions=}")

            # If training image contains exactly one face
            if len(predictions)>0 and predictions[0] :

                pred_name = person == predictions[0][0]
                y.append(True)
                y_pred.append(pred_name)
            else:
                y.append(True)
                y_pred.append(False)
        # Matriz de confusión y precisión
    print(f"{len(y_pred)} {y_pred=} ")
    print(f"{len(y)} {y=}")
    matrix = confusion_matrix(y, y_pred)
    accuracy = accuracy_score(y, y_pred)

    print("Confusion Matrix:")
    print(matrix)
    print("Accuracy:", accuracy)
    print(f"{X_test=} , {y=}")
    return Response("Migration successfull")