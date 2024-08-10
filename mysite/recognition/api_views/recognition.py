# ViewSets define the view behavior.

from utils.exceptions.image_exception import InvalidFileExtensionError
from recognition.models import Face
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.utils.datastructures import MultiValueDictKeyError
import face_recognition

from rest_framework.parsers import FileUploadParser

@api_view(['POST'])
def recognition(request):
    """
    Consulta el rostro por medio de una imagen, `Face` buscará el rostro en la base de datos y retornará el modelo
    """
    queryset = Face.objects.all()
    print(request.FILES , "aaaa")
    
    try:
        face = request.FILES['face']
        file_name = face.name
        file_extension = file_name.split('.')[-1]
        if file_extension not in ["jpg","jpeg","png"]:
            raise InvalidFileExtensionError(f"File extension '{file_extension}' is not allowed.")
        

        
        # Cargar la imagen desde el archivo
        new_image = face_recognition.load_image_file(face)

        # Obtener las codificaciones faciales de la nueva imagen
        face_encodings = face_recognition.face_encodings(new_image)

        if not face_encodings:
            #default_storage.delete(file_path)
            print("No se encotró")
            return Response("No se encotró rostro en la imagen", 400)
        # Cargar todas las codificaciones faciales conocidas de la base de datos
        known_face_encodings = []
        known_face_names = []

        for person in Face.objects.all():
            if not person.face_encoding:
                continue
            known_face_encodings.append([float(val) for val in person.face_encoding.split(',')])
            known_face_names.append({"id":person.id, "metadata":person.metadata, "nombre":person.name})

        # Comprobar cada codificación facial en la nueva imagen
        for face_encoding in face_encodings:
            # TODO GET SCORE
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            print(f"{matches}=")
            name = "Desconocido"

            if True in matches:
                first_match_index = matches.index(True)
                print("first_match_index", first_match_index)
                print("known_face_names", known_face_names)
                print("known_face_names[first_match_index]", known_face_names[first_match_index])
                name = known_face_names[first_match_index]
                
                """ if first_match_index > 1:
                    return Response("Rostro desconocido", 400) """
                    
                
                return Response({
                        "user":name
                    }, 200)
                
            # Eliminar la imagen temporal
            #default_storage.delete(file_path)

    except MultiValueDictKeyError:
        print("No hay archivo")
        return Response({"error":"El archivo Face es requerida"}, 400)

    except InvalidFileExtensionError as fe:
        print(fe)
        return Response("La extensión no es permitida", 400)
    
    except:
        
        print("Error")
        return Response("Error", 500)
