# ViewSets define the view behavior.
import time
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import os
from mysite.settings import MEDIA_ROOT
from recognition.models import Face, FaceTraining
from recognition.ml.knn_recognition import  predict, train
from recognition.models import StatusFace
from sklearn.metrics import confusion_matrix, accuracy_score

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_knn(request):
    start_time = time.time()
    print("Training KNN classifier...")
    client = request.auth.get('client')
    people_training = Face.objects.filter(client=client, status=StatusFace.ACT)
    known_faces_path = f"{MEDIA_ROOT}test_dataset/known_faces"
    unknown_faces_path = f"{MEDIA_ROOT}test_dataset/unknown_faces"
    model_knn = train(people_training, n_neighbors=3, client_id=client)
    test_dir = os.listdir(known_faces_path)
    X_test = []
    y = []
    y_pred = []

    # Loop through each person in the training directory known
    for person in test_dir:
        pix = os.listdir(f"{known_faces_path}/{person}" )

        # Loop through each training image for the current person
        for person_img in pix:
            X_test.append([person,person_img])
            path_img = f"{known_faces_path}/{person}/{person_img}"
            predictions = predict(path_img, model_knn)
            # If training image contains exactly one face
            if len(predictions)>0 and predictions[0] :
                pred_name = person == predictions[0][0]
                y.append(True)
                y_pred.append(pred_name)
            else:
                y.append(True)
                y_pred.append(False)

    pix_unknown = os.listdir(unknown_faces_path)
    # Loop through each person in the training directory unknown
    for person_img in pix_unknown:

        X_test.append(["unknown", person_img])
        # Get the face encodings for the face in each image file
        path_img = f"{unknown_faces_path}/{person_img}"
        predictions = predict(path_img, model_knn)
        # If training image contains exactly one face
        if len(predictions) > 0 and predictions[0][0] is not False:
            y.append(False)
            y_pred.append(True)
        else:
            y.append(False)
            y_pred.append(False)

    # Matriz de confusión y precisión
    matrix = confusion_matrix(y, y_pred)
    accuracy = accuracy_score(y, y_pred)

    print("Confusion Matrix:")
    print(matrix)
    print("Accuracy:", accuracy)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {execution_time} segundos")

    return Response("Stats successfull")