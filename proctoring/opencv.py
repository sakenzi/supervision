import cv2
import mediapipe as mp
import time
import os
import math


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, 
    max_num_faces=1, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Ошибка: не удалось открыть камеру")
    exit()

prev_time = 0
ANGLE_THRESHOLD = 25  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = face_landmarks.landmark[33]   
            right_eye = face_landmarks.landmark[263] 
            nose = face_landmarks.landmark[1]       

            lx, ly = int(left_eye.x * w), int(left_eye.y * h)
            rx, ry = int(right_eye.x * w), int(right_eye.y * h)
            nx, ny = int(nose.x * w), int(nose.y * h)

            dx = rx - lx
            dy = ry - ly
            angle = math.degrees(math.atan2(dy, dx))

            if abs(angle) > ANGLE_THRESHOLD:
                print(f"Голова повернута! Угол: {int(angle)}° — Завершаем работу...")
                cap.release()
                cv2.destroyAllWindows()
                exit()

            cv2.circle(frame, (lx, ly), 5, (255, 0, 0), -1)  
            cv2.circle(frame, (rx, ry), 5, (0, 255, 0), -1)  
            cv2.circle(frame, (nx, ny), 5, (0, 0, 255), -1)  
            cv2.putText(frame, f"Angle: {int(angle)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Proctoring", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
