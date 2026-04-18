# import cv2
# import time
# import numpy as np
# import winsound

# def challenge_response_auth():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         return False
        
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
#     blink_count = 0
#     eyes_present = True # Tracks current state to detect a full "down-up" blink
    
#     print("Blink 3 times to authorize payment...")

#     while blink_count < 3:
#         ret, frame = cap.read()
#         if not ret: break
        
#         frame = cv2.flip(frame, 1)
#         h, w, _ = frame.shape
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
#         # Detect eyes
#         eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

#         # UI: Top Center display
#         cv2.putText(frame, f"BLINKS: {blink_count} / 3", (w//2-100, 50), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#         cv2.putText(frame, "BLINK TO CONFIRM PAYMENT", (w//2-160, h-30), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

#         # Logic: Detect state change
#         if len(eyes) == 0:
#             if eyes_present: # Transition from Open to Closed
#                 eyes_present = False
#         else:
#             if not eyes_present: # Transition from Closed back to Open
#                 blink_count += 1
#                 winsound.Beep(800, 100) # Short beep for each registered blink
#                 eyes_present = True

#         cv2.imshow("BioPay Secure Payment", frame)
        
#         if cv2.waitKey(1) == 27: # ESC to cancel
#             cap.release()
#             cv2.destroyAllWindows()
#             return False

#     # --- FINAL SUCCESS ---
#     ret, frame = cap.read()
#     frame = cv2.flip(frame, 1)
#     cv2.rectangle(frame, (0,0), (w,h), (0, 255, 0), 20)
#     cv2.putText(frame, "PAYMENT AUTHORIZED", (w//2-180, h//2), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
#     cv2.imshow("BioPay Secure Payment", frame)
#     cv2.waitKey(1500)
    
#     cap.release()
#     cv2.destroyAllWindows()
#     return True

import cv2
import time
import numpy as np
import winsound
import random

def challenge_response_auth():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False
        
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    # SECURITY: Generate a random challenge (user must blink N times)
    required_blinks = random.randint(2, 4)
    blink_count = 0
    eyes_present = True
    
    # Security Timing
    start_time = time.time()
    timeout = 15.0 # User has 15 seconds to complete the challenge

    print(f"SECURITY CHALLENGE: BLINK {required_blinks} TIMES")

    while blink_count < required_blinks:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Security UI: Scanning HUD
        # Top HUD Bar
        cv2.rectangle(frame, (0, 0), (w, 80), (20, 20, 20), -1)
        cv2.putText(frame, "BIOMETRIC AUTHENTICATION ACTIVE", (20, 30), 1, 1, (0, 255, 0), 1)
        
        # Central Targeting Ellipse
        cv2.ellipse(frame, (w//2, h//2), (180, 230), 0, 0, 360, (100, 100, 100), 1)
        
        # Challenge Instruction
        cv2.putText(frame, f"CHALLENGE: BLINK {required_blinks} TIMES", (w//2-180, 70), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2)
        
        # Progress Bar
        progress_w = int((blink_count / required_blinks) * 200)
        cv2.rectangle(frame, (w//2-100, h-50), (w//2+100, h-30), (50, 50, 50), -1)
        cv2.rectangle(frame, (w//2-100, h-50), (w//2-100 + progress_w, h-30), (0, 255, 0), -1)

        # SECURITY: Timeout Check
        if time.time() - start_time > timeout:
            print("AUTH FAILED: TIMEOUT")
            cap.release()
            cv2.destroyAllWindows()
            return False

        # Eye Detection
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

        # Logic: Detect state change with Liveness Feedback
        if len(eyes) == 0:
            if eyes_present:
                eyes_present = False
                # Visual feedback that eyes are "captured"
                cv2.circle(frame, (50, h-40), 10, (0, 0, 255), -1) 
        else:
            if not eyes_present:
                blink_count += 1
                winsound.Beep(1200, 80) # Sharper security beep
                eyes_present = True

        cv2.imshow("BioPay Secure Gate", frame)
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            return False

    # --- FINAL SUCCESS ANIMATION ---
    for i in range(10): # Flicker effect
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        color = (0, 255, 0) if i % 2 == 0 else (0, 100, 0)
        cv2.rectangle(frame, (0,0), (w,h), color, 20)
        cv2.putText(frame, "IDENTITY VERIFIED", (w//2-180, h//2), 1, 2, (0, 255, 0), 3)
        cv2.imshow("BioPay Secure Gate", frame)
        cv2.waitKey(100)
    
    cap.release()
    cv2.destroyAllWindows()
    return True