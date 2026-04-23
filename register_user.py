# import cv2
# import os

# def register_face(username):
#     path = f"dataset/{username}"
#     os.makedirs(path, exist_ok=True)

#     cam = cv2.VideoCapture(0)
#     detector = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#     )

#     count = 0
#     while True:
#         ret, frame = cam.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.3, 5)

#         for (x,y,w,h) in faces:
#             count += 1
#             cv2.imwrite(f"{path}/{count}.jpg", gray[y:y+h, x:x+w])
#             cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

#         cv2.imshow("Register Face", frame)
#         if cv2.waitKey(1) == 27 or count >= 40:
#             break

#     cam.release()
#     cv2.destroyAllWindows()


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
SECRET_KEY = b'6f_X-33p_kX-L1_Z8R-9_rW8_L3_M-pQ-X8_R-w_8_M='
cipher = Fernet(SECRET_KEY)


def register_user(full_name, email, mobile, native_city, bank_name, security_qna, password, personal_pin: str):
    """
    Enroll a new BioPay user.

    Parameters
    ----------
    personal_pin : str
        4-digit numeric PIN chosen by the user during registration.
        Stored hashed (SHA-256) — never in plain text.
    """
    import hashlib

    safe_name = email.replace("@", "_").replace(".", "_")
    path = f"dataset/{safe_name}"
    os.makedirs(path, exist_ok=True)

    # ── 1. Validate PIN ────────────────────────────────────────────────────
    if not personal_pin.isdigit() or len(personal_pin) != 4:
        raise ValueError("PIN must be exactly 4 numeric digits.")

    # Store as SHA-256 hash for security
    pin_hash = hashlib.sha256(personal_pin.encode()).hexdigest()

    # ── 2. Build user profile ──────────────────────────────────────────────
    clean_name = full_name.split()[0].lower()
    unique_id  = f"{clean_name}.{mobile[-4:]}@{bank_name.lower()}"

    user_data = {
        "full_name":          full_name,
        "unique_id":          unique_id,
        "balance":            5000,
        "email":              email,
        "password":           password,
        "personal_pin_hash":  pin_hash,       # ← NEW: hashed PIN
        "failed_attempts":    0,
        "security_questions": security_qna,
        "transactions":       [],
        "registered_at":      datetime.now().isoformat(),
    }

    with open(f"{path}/user.json", "w") as f:
        json.dump(user_data, f, indent=4)

    # ── 3. Encrypted QR code ───────────────────────────────────────────────
    encrypted_id_bytes = cipher.encrypt(unique_id.encode("utf-8"))
    scrambled_text     = encrypted_id_bytes.decode("utf-8")
    qrcode.make(scrambled_text).save(f"{path}/qr_code.png")

    # ── 4. Camera & AI face + eye capture ─────────────────────────────────
    cam          = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    scan_line_y = 0
    face_count  = 0
    eye_count   = 0
    h           = 480   # fallback height before first frame

    # ── STAGE 1: FACE STRUCTURE SCAN (30 frames) ──────────────────────────
    while face_count < 30:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        scan_line_y = (scan_line_y + 12) % h
        cv2.line(frame, (0, scan_line_y), (w, scan_line_y), (0, 255, 0), 2)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, fw, fh) in faces:
            color = (255, 255, 255)
            for i in range(x, x + fw, fw // 4):
                cv2.line(frame, (i, y), (i, y + fh), color, 1)
            for i in range(y, y + fh, fh // 4):
                cv2.line(frame, (x, i), (x + fw, i), color, 1)
            cv2.line(frame, (x, y),    (x + fw, y + fh), color, 1)
            cv2.line(frame, (x + fw, y), (x, y + fh),   color, 1)
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 255, 0), 2)

            face_count += 1
            cv2.imwrite(f"{path}/face_{face_count}.jpg", gray[y:y + fh, x:x + fw])
            if face_count == 1:
                cv2.imwrite(f"{path}/profile.jpg", frame)

        cv2.putText(frame, f"ANALYZING STRUCTURE: {face_count}/30",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("BIOPAY ADVANCED ENROLLMENT", frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyWindow("BIOPAY ADVANCED ENROLLMENT")

    # ── STAGE 2: EYE CAPTURE (20 frames) ─────────────────────────────────
    while eye_count < 20:
        ret, frame = cam.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        scan_line_y = (scan_line_y + 20) % h
        cv2.line(frame, (0, scan_line_y), (w, scan_line_y), (255, 255, 0), 2)

        eyes = eye_cascade.detectMultiScale(gray, 1.3, 10)
        for (x, y, ew, eh) in eyes:
            eye_count += 1
            cv2.imwrite(f"{path}/eyes_{eye_count}.jpg", gray[y:y + eh, x:x + ew])
            cv2.rectangle(frame, (x, y), (x + ew, y + eh), (255, 255, 0), 2)

        cv2.putText(frame, f"EYE CAPTURE: {eye_count}/20",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("EYE BIOMETRIC DATA", frame)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


# -------------------------------------------------
# SECURE QR SCANNER
# -------------------------------------------------
def scan_biopay_qr() -> str:
    """Scan a BioPay encrypted QR code and return the decrypted Bio-ID."""
    cap      = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    data     = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        scrambled_data, bbox, _ = detector.detectAndDecode(frame)

        if scrambled_data:
            try:
                decrypted_id = cipher.decrypt(scrambled_data.encode("utf-8")).decode("utf-8")
                data = decrypted_id

                cv2.rectangle(frame, (100, 100), (540, 380), (0, 255, 0), 3)
                cv2.putText(frame, "SECURE ID DECRYPTED", (150, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("BioPay Secure Scanner", frame)
                cv2.waitKey(1000)
                break
            except Exception:
                cv2.putText(frame, "ACCESS DENIED: INVALID QR", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("BioPay Secure Scanner", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return data