import cv2
import pickle
import os
import time
import numpy as np

def enhance_frame(frame):
    """
    Boosts luminance and contrast using CLAHE (Contrast Limited Adaptive 
    Histogram Equalization) to reveal facial features in dark rooms.
    """
    img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
    enhanced_frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return enhanced_frame

def authenticate(selected_user):
    if not os.path.exists("model/face_model.yml"):
        return False, 999
    
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("model/face_model.yml")
    
    with open("model/labels.pkl", "rb") as f: 
        label_map = pickle.load(f)
    
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    cam = cv2.VideoCapture(0)
    start = time.time()
    best_conf = 999  # Track the most accurate match found during the 15s window

    while time.time() - start < 15:
        ret, raw_frame = cam.read()
        if not ret: break
        
        # Apply low-light enhancement
        frame = enhance_frame(raw_frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            lab_id, conf = model.predict(gray[y:y+h, x:x+w])
            predicted_folder = label_map.get(lab_id)

            if predicted_folder == selected_user:
                if conf < best_conf:
                    best_conf = conf

                # Success threshold
                if conf < 50:
                    cam.release()
                    cv2.destroyAllWindows()
                    return True, conf
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(frame, "Match Weak - Move Closer", (x, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown Identity", (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("BioPay Secure Scan (Low-Light Mode)", frame)
        if cv2.waitKey(1) == 27: break
        
    cam.release()
    cv2.destroyAllWindows()
    return False, best_conf