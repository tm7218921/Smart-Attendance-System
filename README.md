# Smart-attendance-System
A real-time attendance tracking solution leveraging face recognition technology to automate the process. Built using OpenCV, Dlib, and Pandas, this system ensures accurate attendance management and defaulter identification.

**Features**
*Face Detection and Recognition*: Utilizes advanced algorithms for reliable identification.
*Streamlit Interface*: Provides separate login portals for teachers and students with role-based access.
*Attendance Management*: Tracks and records attendance in CSV files, marking defaulters automatically.
*Error Resolution*: Optimized embedding processing and resolved broadcasting shape mismatches for seamless operation.

**Technologies Used**
Python
OpenCV, Dlib
Pandas
Streamlit
**Future Enhancements**
Integration with external databases.
Real-time notifications for defaulters.
Enhanced security for role-based access.


You Have to use Your own Dataset Or Use any other Dataset from kaggle or other sites.

File Descriptions and Functions:

1. BACKEND_LOGIC.py: Contains the core functions that integrate various modules, manage data flow, and handle the main operations of the system.

2. DATA_PREPROCESSING.py: Responsible for preparing and cleaning the dataset, including tasks like normalization and encoding, to ensure optimal performance of the recognition algorithms.

3. REAL_TIME_FACE_DETECTION.py: Handles the live video feed, detects faces in real-time using OpenCV and Dlib, and passes the detected faces to the recognition module.

4. SCHEDULE.py: Manages scheduling-related functionalities, such as defining class times, tracking attendance periods, and generating reports based on the schedule.

5. SVM.py: Implements a Support Vector Machine (SVM) model for classifying and recognizing faces based on extracted features, enhancing the accuracy of the recognition process.

6. UI.py: Develops the user interface, providing interactive elements for users to interact with the system, view attendance records, and manage settings.

7. dlib_face_recognition_resnet_model_v1.dat: A pre-trained model file from Dlib used for extracting high-quality face embeddings necessary for recognition tasks.

8. face_embeddings.pkl: A serialized file containing the face embeddings of enrolled individuals, used by the recognition system to match and identify faces.

9. haarcascade_frontalface_default.xml: An XML file containing pre-trained data for detecting frontal faces, utilized by OpenCV's Haar Cascade classifier.

10. shape_predictor_68_face_landmarks.dat: A Dlib model file used to detect facial landmarks, aiding in precise face alignment and feature extraction.

11. svm_face_recognition_model.pkl: A serialized SVM model trained on the face embeddings, used to predict and recognize individuals during the attendance process.

12. try.py: A script likely used for testing and experimentation purposes, containing code snippets to validate functionalities during development.

This system streamlines attendance management by automating the recognition process, reducing manual errors, and providing real-time tracking and reporting capabilities.
