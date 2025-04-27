
import cv2
import dlib
import time
import requests
import urllib.request
import numpy as np
from pygame import mixer
from imutils import face_utils
from scipy.spatial import distance
import imutils

ESP32_URL = "http://192.168.244.45"
EAR_THRESH = 0.30
CONSEC_FRAMES = 8
flag = 0
buzz_triggered = False

mixer.init()
mixer.music.load("music.wav")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def trigger_buzz_on():
    try:
        res = requests.get(f"{ESP32_URL}/buzz_on", timeout=1)
        print("Buzzer ON:", res.text)
    except Exception as e:
        print("Buzzer ON error:", e)

def trigger_buzz_off():
    try:
        res = requests.get(f"{ESP32_URL}/buzz_off", timeout=1)
        print("Buzzer OFF:", res.text)
    except Exception as e:
        print("Buzzer OFF error:", e)

def update_led(state):
    try:
        res = requests.get(f"{ESP32_URL}/led?state={state}", timeout=1)
        print(f"LED {state}:", res.text)
    except Exception as e:
        print("LED error:", e)

def update_lcd(message):
    try:
        safe_msg = requests.utils.quote(message)
        res = requests.get(f"{ESP32_URL}/lcd?text={safe_msg}", timeout=1)
        print("LCD:", res.text)
    except Exception as e:
        print("LCD error:", e)

while True:
    try:
        img_resp = urllib.request.urlopen(f"{ESP32_URL}/capture", timeout=5)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)

        if frame is None:
            print("Empty frame")
            continue

        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)

        for face in faces:
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

            cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

            cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            if ear < EAR_THRESH:
                flag += 1
                if flag >= CONSEC_FRAMES:
                    cv2.putText(frame, "!!! DROWSINESS ALERT !!!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    trigger_buzz_on()
                    update_led("red")
                    update_lcd("Drowsiness Alert!")
                    if not buzz_triggered:
                        mixer.music.play()
                        buzz_triggered = True
            else:
                flag = 0
                buzz_triggered = False
                mixer.music.stop()
                trigger_buzz_off()
                update_led("green")
                update_lcd("Driver Active")

        cv2.imshow("Driver Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.05)

    except Exception as e:
        print("Error:", e)
        continue

cv2.destroyAllWindows()
