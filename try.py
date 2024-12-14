import cv2
import dlib
import numpy as np

# Load face detector and landmark predictor
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


# Function to calculate EAR (Eye Aspect Ratio) for blink detection
def calculate_ear(eye_points):
    eye_points = np.array([[p.x, p.y] for p in eye_points])
    A = np.linalg.norm(eye_points[1] - eye_points[5])  # Vertical distance
    B = np.linalg.norm(eye_points[2] - eye_points[4])  # Vertical distance
    C = np.linalg.norm(eye_points[0] - eye_points[3])  # Horizontal distance

    # Calculate EAR
    ear = (A + B) / (2.0 * C)
    return ear


# Function to check for blinks and draw rectangles around eyes
def detect_blink(frame, blink_threshold=0.25):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    blink_detected = False

    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Get landmarks for the detected face
        landmarks = predictor(gray, dlib.rectangle(x, y, x + w, y + h))

        # Get left and right eye landmarks
        left_eye = [landmarks.part(i) for i in range(36, 42)]  # Left eye landmarks
        right_eye = [landmarks.part(i) for i in range(42, 48)]  # Right eye landmarks

        # Draw rectangles around the eyes
        left_eye_rect = cv2.boundingRect(np.array([(p.x, p.y) for p in left_eye]))
        right_eye_rect = cv2.boundingRect(np.array([(p.x, p.y) for p in right_eye]))

        cv2.rectangle(frame, (left_eye_rect[0] + x, left_eye_rect[1] + y),
                      (left_eye_rect[0] + left_eye_rect[2] + x, left_eye_rect[1] + left_eye_rect[3] + y), (0, 255, 0),
                      2)

        cv2.rectangle(frame, (right_eye_rect[0] + x, right_eye_rect[1] + y),
                      (right_eye_rect[0] + right_eye_rect[2] + x, right_eye_rect[1] + right_eye_rect[3] + y),
                      (0, 255, 0), 2)

        # Calculate EAR for both eyes
        ear_left = calculate_ear(left_eye)
        ear_right = calculate_ear(right_eye)

        # Check if both eyes are closed
        if ear_left < blink_threshold and ear_right < blink_threshold:
            blink_detected = True

    return blink_detected


# Main loop for video capture
cap = cv2.VideoCapture(0)

# Frame counter and blink detection variables
blink_counter = 0
blink_threshold = 5  # Number of frames to count as a blink

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if detect_blink(frame):
        blink_counter += 1
    else:
        blink_counter = 0  # Reset if no blink detected

    if blink_counter >= blink_threshold:
        cv2.putText(frame, "Real User", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Spoof Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Spoof Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
