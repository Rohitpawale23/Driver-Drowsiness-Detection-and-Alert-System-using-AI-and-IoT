import cv2
import urllib.request
import numpy as np

# Load Haar Cascade Classifiers
f_cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Update with the correct ESP32-CAM URL
url = 'http://192.168.0.102/capture'  # Try /cam-lo.jpg or /cam-hi.jpg if this doesn't work
cv2.namedWindow("Live Transmission", cv2.WINDOW_AUTOSIZE)

while True:
    try:
        # Get image from ESP32-CAM
        img_resp = urllib.request.urlopen(url, timeout=5)  # 5 seconds timeout
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        # Check if the image was decoded successfully
        if img is None:
            print("Failed to decode image. Check URL or connection.")
            continue
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = f_cas.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            # Detect eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # Display the image
        cv2.imshow("Live Transmission", img)

    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except cv2.error as e:
        print(f"OpenCV Error: {e}")

    # Press 'q' to quit
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
