# Driver-Drowsiness-Detection-and-Alert-System-using-AI-and-IoT 🚗💤
Real-time Driver Drowsiness Detection and Alert System using AI and IoT. Combines ESP32-CAM, Python, and facial landmarks to ensure road safety with instant in-vehicle alerts.


📚 Project Overview:

Fatigue while driving is a serious cause of road accidents globally. This project aims to prevent drowsiness-induced accidents by continuously monitoring the driver’s eyes using a camera (ESP32-CAM), processing facial landmarks using AI, and triggering instant audio-visual alerts when signs of sleepiness are detected.
The system uses Eye Aspect Ratio (EAR) calculation to detect drowsiness in real-time and activates a buzzer, LED indicators, and LCD display to alert the driver and nearby vehicles. All components are affordable, lightweight, and work seamlessly over Wi-Fi using HTTP requests.




## 🚀 Features:

📷 Real-time eye monitoring with ESP32-CAM

🧠 AI-based EAR (Eye Aspect Ratio) computation

🔔 Instant alerts: buzzer sound + LED blinking + LCD messages

📡 Wi-Fi-based HTTP control for alerts

⚡ Lightweight and low-cost hardware setup



## 🛠 Technologies and Components Used:

Hardware Used-->

  - ESP32-CAM Module	
  - Active Buzzer 
  - Red and Green LEDs
  - 16x2 LCD Display (I2C) 
  - FTDI Programmer	
  - 220-ohm Resistors


Software Used-->

  - Python 3.8+
  - OpenCV
  - Dlib
  - Imutils
  - Pygame Mixer
  - Requests


## 📸 Snapshots:

 - Real-time eye tracking
  ![WhatsApp Image 2025-04-16 at 22 15 47_3b1204d4](https://github.com/user-attachments/assets/3254f880-e5b2-40ce-bb06-3a2a6ad0461e)



 - LCD displaying driver status
   ![WhatsApp Image 2025-04-19 at 01 23 49_4554ddc7](https://github.com/user-attachments/assets/c4144429-2575-46c0-a3fe-9e8d857bb204)
  


 - Buzzer and LEDs activating on drowsiness detection
    ![WhatsApp Image 2025-04-19 at 01 23 47_48e6cd89](https://github.com/user-attachments/assets/11769678-3d6f-4274-9bcc-62b282c691b6)
    ![WhatsApp Image 2025-04-27 at 21 50 08_d7a64eeb](https://github.com/user-attachments/assets/7efb0e6f-2cf3-40cb-b9ae-616cd0618e6e)


## 🔥 How It Works:

- ESP32-CAM captures real-time video and hosts a local HTTP server.
- Python script fetches the frame, detects facial landmarks using Dlib.
- Computes Eye Aspect Ratio (EAR) to monitor blinking patterns.
- If EAR drops below a threshold (0.30) for 8+ consecutive frames:
- Activates buzzer, red LED, and drowsiness alert on LCD.
- If EAR rises (normal open eyes):
- Activates green LED and displays Driver Active message.



# 🙌 Developed By:

**Team A2-4:**

- Rohit Pawale
- Vaibhav Kangane
- Om Pardesi



## 🚀 Let’s make roads smarter and safer with AI and IoT!🛣️
