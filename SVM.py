import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

with open("face_embeddings.pkl", "rb") as f:
    embeddings, labels = pickle.load(f)

x = embeddings
y = labels

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = SVC(kernel='linear', probability=True)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
print(classification_report(y_test, y_pred))

joblib.dump(model, 'svm_face_recognition_model.pkl')
