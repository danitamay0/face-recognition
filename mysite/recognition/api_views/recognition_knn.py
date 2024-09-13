# ViewSets define the view behavior.

from recognition.ml.knn_recognition import predict, train
from mysite.settings import MEDIA_ROOT, MODEL_ROOT
from utils.exceptions.image_exception import InvalidFileExtensionError
from recognition.models import Face, FacePredict, StatusFace
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.datastructures import MultiValueDictKeyError

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recognition_knn(request):
    try:
        client = request.auth.get('client')
        unknow_face = request.FILES['face']
        file_name = unknow_face.name
        file_extension = file_name.split('.')[-1]
        if file_extension not in ["jpg","jpeg","png"]:
            raise InvalidFileExtensionError(f"File extension '{file_extension}' is not allowed.")
            
        people_training =  Face.objects.filter(client = client, status=StatusFace.ACT)
        model_save_path = f"{MODEL_ROOT}/{client}/trained_knn_model.clf"
        
        train( people_training , model_save_path=model_save_path, n_neighbors=3, client_id = client )
        print("Training complete!")

        predictions = predict(unknow_face, model_path=model_save_path)

        # Print results on the console
        for name, (top, right, bottom, left) in predictions:
            print("- Found {} at ({}, {})".format(name, left, top))
            if name == "unknown":
                continue
            
            face_ = people_training.filter(id=name).first()
            face_prediction = None
            
            if face_:
                print(face_)
                face_prediction=face_.id
                FacePredict( found_face=True, face_id=face_prediction, client_id = client, image=unknow_face ).save()
                return Response({
                            "user":{"id":face_.id, "metadata":face_.metadata, "nombre":face_.name},
                            "detected": True
                        }, 200)
            FacePredict( found_face=False, face=None, client_id = client, image=unknow_face ).save()
            return Response("Face not found ", 40)
        
        FacePredict( found_face=False, face=None, client_id = client, image=unknow_face ).save()
        return Response("Face not found ", 400)
                
    
    except MultiValueDictKeyError:
        print("No hay archivo")
        return Response({"error":"El archivo Face es requerida"}, 400)

    except InvalidFileExtensionError as fe:
        print(fe)
        return Response("La extensión no es permitida", 415)
    
    except Exception as e:
        print("Error", e)
        return Response("Error", 500)


