import cv2
import os
import json
import qrcode
import numpy as np
from datetime import datetime
from cryptography.fernet import Fernet

# -------------------------------------------------
# AES ENCRYPTION SETUP
# -------------------------------------------------
# This key must remain the same for encryption and decryption.
# For the demo, we use this fixed Fernet-compatible key.
SECRET_KEY = b'6f_X-33p_kX-L1_Z8R-9_rW8_L3_M-pQ-X8_R-w_8_M=' 
cipher = Fernet(SECRET_KEY)

def register_user(full_name, email, mobile, native_city, bank_name, security_qna, password):
    safe_name = email.replace("@", "_").replace(".", "_")
    path = f"dataset/{safe_name}"
    os.makedirs(path, exist_ok=True)

    # 1. Metadata & ID Generation
    clean_name = full_name.split()[0].lower()
    unique_id = f"{clean_name}.{mobile[-4:]}@{bank_name.lower()}"
    
    user_data = {
        "full_name": full_name, 
        "unique_id": unique_id, 
        "balance": 5000, 
        "email": email,
        "password": password,  # NEW: Store Password
        "failed_attempts": 0,
        "security_questions": security_qna
    }
    
    with open(f"{path}/user.json", "w") as f:
        json.dump(user_data, f, indent=4)

    # --- 🛡️ NEW ENCRYPTION LOGIC START ---
    # We encrypt the ID and then convert it to a string for the QR Generator
    encrypted_id_bytes = cipher.encrypt(unique_id.encode('utf-8'))
    scrambled_text = encrypted_id_bytes.decode('utf-8') 
    
    # This will now show as gibberish (e.g., gAAAAAB...) on your phone camera
    qrcode.make(scrambled_text).save(f"{path}/qr_code.png")
    # --- 🛡️ NEW ENCRYPTION LOGIC END ---

    # 2. Camera & AI Setup
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    
    scan_line_y = 0
    face_count = 0
    eye_count = 0

    # ================= STAGE 1: FACE STRUCTURE SCAN (30 PICS) =================
    while face_count < 30:
        ret, frame = cam.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Top-to-Bottom Scanner Line
        scan_line_y += 12
        if scan_line_y > h: scan_line_y = 0
        cv2.line(frame, (0, scan_line_y), (w, scan_line_y), (0, 255, 0), 2) 

        # Detect Face & Draw Structure Lines
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, fw, fh) in faces:
            color = (255, 255, 255) 
            for i in range(x, x + fw, fw//4):
                cv2.line(frame, (i, y), (i, y + fh), color, 1)
            for i in range(y, y + fh, fh//4):
                cv2.line(frame, (x, i), (x + fw, i), color, 1)
            cv2.line(frame, (x, y), (x+fw, y+fh), color, 1)
            cv2.line(frame, (x+fw, y), (x, y+fh), color, 1)
            cv2.rectangle(frame, (x,y), (x+fw, y+fh), (0, 255, 0), 2)

            face_count += 1
            cv2.imwrite(f"{path}/face_{face_count}.jpg", gray[y:y+fh, x:x+fw])
            if face_count == 1: cv2.imwrite(f"{path}/profile.jpg", frame)

        cv2.putText(frame, f"ANALYZING STRUCTURE: {face_count}/30", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("BIOPAY ADVANCED ENROLLMENT", frame)
        if cv2.waitKey(1) == 27: break

    cv2.destroyWindow("BIOPAY ADVANCED ENROLLMENT")

    # ================= STAGE 2: EYE CAPTURE (20 PICS) =================
    while eye_count < 20:
        ret, frame = cam.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        scan_line_y += 20
        if scan_line_y > h: scan_line_y = 0
        cv2.line(frame, (0, scan_line_y), (w, scan_line_y), (255, 255, 0), 2)

        eyes = eye_cascade.detectMultiScale(gray, 1.3, 10)
        for (x, y, ew, eh) in eyes:
            eye_count += 1
            cv2.imwrite(f"{path}/eyes_{eye_count}.jpg", gray[y:y+eh, x:x+ew])
            cv2.rectangle(frame, (x,y), (x+ew, y+eh), (255, 255, 0), 2)
        
        cv2.putText(frame, f"EYE CAPTURE: {eye_count}/20", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("EYE BIOMETRIC DATA", frame)
        if cv2.waitKey(1) == 27: break

    cam.release()
    cv2.destroyAllWindows()

# -------------------------------------------------
# SECURE QR SCANNER (DECRYPTING IN REAL-TIME)
# -------------------------------------------------
def scan_biopay_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    data = ""
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        
        # Read Scrambled Data
        scrambled_data, bbox, _ = detector.detectAndDecode(frame)
        
        if scrambled_data:
            try:
                # DECRYPT using the same Secret Key
                decrypted_id = cipher.decrypt(scrambled_data.encode('utf-8')).decode('utf-8')
                data = decrypted_id
                
                # Feedback Success
                cv2.rectangle(frame, (100, 100), (540, 380), (0, 255, 0), 3)
                cv2.putText(frame, "SECURE ID DECRYPTED", (150, 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("BioPay Secure Scanner", frame)
                cv2.waitKey(1000)
                break
            except:
                cv2.putText(frame, "ACCESS DENIED: INVALID QR", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("BioPay Secure Scanner", frame)
        if cv2.waitKey(1) == 27: break
        
    cap.release()
    cv2.destroyAllWindows()
    return data