# ViewSets define the view behavior.

from mysite.settings import MEDIA_ROOT
from utils.exceptions.image_exception import InvalidFileExtensionError
from recognition.models import Face, FaceTraining
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.utils.datastructures import MultiValueDictKeyError
import face_recognition

from rest_framework.parsers import FileUploadParser

@api_view(['POST'])
def recognition_svm(request):
    """
    Consulta el rostro por medio de una imagen, `Face` buscará el rostro en la base de datos y retornará el modelo
    """
    # Train multiple images per person
    # Find and recognize faces in an image using a SVC with scikit-learn

    """
    Structure:
            <test_image>.jpg
            <train_dir>/
                <person_1>/
                    <person_1_face-1>.jpg
                    <person_1_face-2>.jpg
                    .
                    .
                    <person_1_face-n>.jpg
            <person_2>/
                    <person_2_face-1>.jpg
                    <person_2_face-2>.jpg
                    .
                    .
                    <person_2_face-n>.jpg
                .
                .
                <person_n>/
                    <person_n_face-1>.jpg
                    <person_n_face-2>.jpg
                    .
                    .
                    <person_n_face-n>.jpg
    """

    import face_recognition
    from sklearn import svm
    import os

    # Training the SVC classifier

    # The training data would be all the face encodings from all the known images and the labels are their names
    
    
    encodings = []
    names = []

    unknow_face = request.FILES['face']
    file_name = unknow_face.name
    file_extension = file_name.split('.')[-1]
    if file_extension not in ["jpg","jpeg","png"]:
        raise InvalidFileExtensionError(f"File extension '{file_extension}' is not allowed.")
        
    # Training directory
    people_training = Face.objects.all()
    # Loop through each person in the training directory
    for person in people_training:
        #pix = os.listdir(f"/{MEDIA_ROOT}/image/{person}")
        training_faces = FaceTraining.objects.filter(face=person.id)
        # Loop through each training image for the current person
        for person_img in training_faces:
            # Get the face encodings for the face in each image file
            """ face = face_recognition.load_image_file(f"/{MEDIA_ROOT}/image/{person}/{person_img}" )
            face_bounding_boxes = face_recognition.face_locations(face) """
            if not person_img.face_encoding:
                print(person + "/" + person_img + " was skipped and can't be used for training")
                
                continue
            face_enc = [float(val) for val in person_img.face_encoding.split(',')]
            print(face_enc)
            
            encodings.append(face_enc)
            names.append(person.id)
            #If training image contains exactly one face
            """ if len(face_bounding_boxes) == 1:
                print("---------x-------")
                
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                print(f"{person=}, {int(person)}")
                person_1 = int(person)
                encodings.append(face_enc)
                names.append(person_1) """
          
    from sklearn.preprocessing import LabelEncoder
    # Create and train the SVC classifier
    print( f"{names=}")

# Create and train the SVC classifier
    le = LabelEncoder()
    y_labels = le.fit_transform(names)
    THRESHOLD = 0.6  # Este valor puede necesitar ajuste
    clf = svm.SVC(gamma='scale', probability=True)
    clf.fit(encodings,y_labels)

    # Load the test image with unknown faces into a numpy array
    test_image = face_recognition.load_image_file(unknow_face)
    # Find all the faces in the test image using the default HOG-based model
    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    print("Number of faces detected: ", no)

    # Predict all the faces in the test image using the trained classifier
    print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image)[i]
        #distances = clf.decision_function([test_image_enc])
        #distances = clf.predict_proba([test_image_enc])
        #print(f"{distances=}")
        probs = clf.predict_proba([test_image_enc])[0]
        # Encuentra la clase con la mayor distancia al margen de decisión
        #max_distance = max(distances)
        #predicted_class = clf.predict([test_image_enc])[0]
        #predicted_class = clf.predict_proba([test_image_enc])[0]
        #name = clf.predict([test_image_enc])
        
         # Encuentra la clase con la mayor probabilidad
        import numpy as np
        max_prob = max(probs)
        predicted_class = np.argmax(probs)
        name = predicted_class
        print(max_prob)
        if max_prob < THRESHOLD:
            print("Unknown face detected")
            print(f"{name=}")
            
            return Response({
                        "user": None,
                        "detected": False
                    }, 200)
            
        inverse = list(le.inverse_transform([name]))
        if len(inverse) > 0 :
            
            print(f"{name=} {inverse[0]  }")
            face_ = people_training.filter(id=inverse[0]).first()
            print(face_)
            return Response({
                        "user":{"id":face_.id, "metadata":face_.metadata, "nombre":face_.name},
                        "detected": True
                    }, 200)
            
    return Response("Yes")