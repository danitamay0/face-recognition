from mysite.settings import MODEL_ROOT
from recognition.models import FaceTraining
import face_recognition

import math
import pickle
import os
from sklearn.neighbors import KNeighborsClassifier

def train(faces, client_id, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False, ):
    """
    Trains a k-nearest neighbors classifier for face recognition.

    :param faces: List of faces for each known person, with its name.

     Structure:
        <face>/
        ├── <face_trainings1>/
        │   ├── <face_training>.face_encoding
        │   ├── <somename2>.face_encoding
        │   ├── ...
        ├── <face_trainings2>/
        │   ├── <somename1>.face_encoding
        │   └── <somename2>.face_encoding
        └── ...

    :param client_id: to create folder with model by client
    :param model_save_path: (optional) path to save model on disk
    :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
    :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
    :param verbose: verbosity of training
    :return: returns knn classifier that was trained on the given data.
    """
    X = []
    y = []

    for face in faces:
        try:
            face_trains = FaceTraining.objects.filter(face=face.id)

            # Loop through each training image for the current person
            for face_train in face_trains:
                # Convert the face_encoding string to a list of floats
                if face_train.face_encoding:
                    face_bounding_boxes = [float(val) for val in face_train.face_encoding.split(',')]
                    if len(face_bounding_boxes) == 0:
                        # If there are no face encodings, skip the image
                        if verbose:
                            print(f"Image {face_train} not suitable for training: Didn't find a face")
                    else:
                        # Add face encoding for current image to the training set
                        X.append(face_bounding_boxes)
                        y.append(str(face.id))  # Use face.id instead of faces.id
    # Check if X is empty
        except Exception as e:
            print(f"error face: {face} :-> {e}")
    if len(X) == 0:
        raise ValueError("No training data found. Ensure that face encodings are available.")

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)
    # Create and train the KNN classifier
    knn_clf = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:

        if  not os.path.exists(f"{MODEL_ROOT}/{client_id}"):
            os.mkdir(f"{MODEL_ROOT}/{client_id}")
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f) # save binary

    return knn_clf




def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.54):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """

    """ if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))
    """
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else (False, loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

