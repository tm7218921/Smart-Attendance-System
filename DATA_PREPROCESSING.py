import os
import cv2
import dlib
import numpy as np
import pickle

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

dataset_dir = "dataset"

embeddings = []
labels = []

target_size = (224, 224)

for person_dir in os.listdir(dataset_dir):
    person_path = os.path.join(dataset_dir, person_dir)

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)

        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, target_size)
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            embedding = np.array(face_recognizer.compute_face_descriptor(img_resized, landmarks))

            embeddings.append(embedding)
            labels.append(person_dir)

with open("face_embeddings.pkl", "wb") as f:
    pickle.dump((embeddings, labels), f)

print(f"Collected {len(embeddings)} embeddings.")
