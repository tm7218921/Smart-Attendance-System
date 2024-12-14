
import cv2
import dlib
import numpy as np
import joblib
import pickle
import time

svm_model=joblib.load('svm_face_recognition_model.pkl')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

with open("face_embeddings.pkl", "rb") as f:
    embeddings, labels = pickle.load(f)

x = embeddings
y = labels

stored_embeddings=x
stored_embeddings=np.array(stored_embeddings)
stored_labels=y
stored_labels = np.array([str(label) for label in stored_labels])

def euclidean_distance(embedding1, embedding2):
    return np.linalg.norm(embedding1 - embedding2)
threshold=0.5
# url="http://192.168.0.102:8080/video"
cap = cv2.VideoCapture(0)

def get_face_embedding(face_rect, rgb_image):
    shape = predictor(rgb_image, face_rect)
    face_embedding = face_rec_model.compute_face_descriptor(rgb_image, shape)
    return np.array(face_embedding)

start_time = time.time()
detected_faces = []
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.resize(frame, (320, 240))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 5)
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        face_embedding = get_face_embedding(dlib_rect, rgb)

        predicted_label = svm_model.predict([face_embedding])[0]
        label_indices = np.where(stored_labels == predicted_label)[0]
        if label_indices.size > 0:
            label_embeddings = stored_embeddings[label_indices]
        distances = np.array(
            [euclidean_distance(face_embedding, stored_embedding) for stored_embedding in label_embeddings])
        min_distance = np.min(distances)

        if min_distance < threshold:
            person_name = predicted_label
        else:
            person_name = "Unknown"

        cv2.putText(frame, person_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if person_name not in detected_faces:
            detected_faces.append(person_name)

        # print("128D Face Embedding:", face_embedding)

    cv2.imshow('Real Time Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if time.time() - start_time > 30:
        break
item_to_remove="Unknown"
if item_to_remove in detected_faces:
    detected_faces.remove("Unknown")

cap.release()
cv2.destroyAllWindows()
