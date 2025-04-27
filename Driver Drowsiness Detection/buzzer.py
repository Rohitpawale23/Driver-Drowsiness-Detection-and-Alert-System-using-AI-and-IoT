from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import cv2
import urllib.request
import numpy as np
import requests
import time

# Initialize the mixer and load alert sound
mixer.init()
mixer.music.load("music.wav")

# Function to calculate Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Constants and threshold values
thresh = 0.30            # EAR threshold for drowsiness
frame_check = 8         # Number of consecutive frames to trigger alert
flag = 0                 # Count of frames below threshold
buzz_triggered = False   # Track if buzzer has already been triggered

# Load Dlib's face detector and shape predictor
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

# Get indices of left and right eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# ESP32-CAM URL (update this with your IP address)
# url = "http://192.168.167.45/capture"
# url = "http://192.168.167.75/capture"
url = "http://192.168.244.45/capture"

# Start video stream from ESP32-CAM
while True:
    try:
        # Get image from ESP32-CAM
        img_resp = urllib.request.urlopen(url, timeout=5)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)

        # Check if image is valid
        if frame is None:
            print("Failed to decode image. Check URL or connection.")
            continue

        # Resize and convert to grayscale
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        subjects = detect(gray, 0)

        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            # Draw eye contours
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # Display EAR and flag count
            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Frames: {flag}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            # Drowsiness detection logic
            if ear < thresh:
                flag += 1
                if flag >= frame_check:
                    cv2.putText(frame, "********* ALERT! DROWSINESS DETECTED! *********", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if not buzz_triggered:
                        try:
                            # response = requests.get("http://192.168.167.45/buzz", timeout=2)
                            response = requests.get("http://192.168.244.45/buzz", timeout=2)
                            print("Buzzer triggered:", response.text)
                            buzz_triggered = True
                        except Exception as e:
                            print("Failed to trigger buzzer:", e)
            else:
                flag = 0
                buzz_triggered = False
                mixer.music.stop()

        # Display the video stream
        cv2.imshow("Frame", frame)

        # Press 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        time.sleep(0.05)  # Add small delay for ESP32-CAM stability

    except Exception as e:
        print(f"Error: {e}")
        continue

# Release resources
cv2.destroyAllWindows()
