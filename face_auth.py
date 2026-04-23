# import cv2
# import pickle
# import os
# import time
# import numpy as np

# def enhance_frame(frame):
#     """
#     Boosts luminance and contrast using CLAHE (Contrast Limited Adaptive 
#     Histogram Equalization) to reveal facial features in dark rooms.
#     """
#     img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
#     enhanced_frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
#     return enhanced_frame

# def authenticate(selected_user):
#     if not os.path.exists("model/face_model.yml"):
#         return False, 999
    
#     model = cv2.face.LBPHFaceRecognizer_create()
#     model.read("model/face_model.yml")
    
#     with open("model/labels.pkl", "rb") as f: 
#         label_map = pickle.load(f)
    
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
#     cam = cv2.VideoCapture(0)
#     start = time.time()
#     best_conf = 999  # Track the most accurate match found during the 15s window

#     while time.time() - start < 15:
#         ret, raw_frame = cam.read()
#         if not ret: break
        
#         # Apply low-light enhancement
#         frame = enhance_frame(raw_frame)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.3, 5)
        
#         for (x, y, w, h) in faces:
#             lab_id, conf = model.predict(gray[y:y+h, x:x+w])
#             predicted_folder = label_map.get(lab_id)

#             if predicted_folder == selected_user:
#                 if conf < best_conf:
#                     best_conf = conf

#                 # Success threshold
#                 if conf < 50:
#                     cam.release()
#                     cv2.destroyAllWindows()
#                     return True, conf
#                 else:
#                     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
#                     cv2.putText(frame, "Match Weak - Move Closer", (x, y-10), 
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
#             else:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
#                 cv2.putText(frame, "Unknown Identity", (x, y-10), 
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

#         cv2.imshow("BioPay Secure Scan (Low-Light Mode)", frame)
#         if cv2.waitKey(1) == 27: break
        
#     cam.release()
#     cv2.destroyAllWindows()
#     return False, best_conf

# import cv2
# import pickle
# import os
# import time
# import numpy as np
# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# # --- DYNAMIC PATHING ---
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "model", "face_model.yml")
# LABEL_PATH = os.path.join(BASE_DIR, "model", "labels.pkl")

# def enhance_frame(frame):
#     """Boosts luminance for low-light mobile/PC environments."""
#     img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
#     return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

# def authenticate(selected_user):
#     # Check if we are running in Streamlit Cloud
#     IS_CLOUD = os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud"

#     if not os.path.exists(MODEL_PATH):
#         st.error("Face model not found. Please train the model first.")
#         return False, 999

#     # Load Model and Labels
#     model = cv2.face.LBPHFaceRecognizer_create()
#     model.read(MODEL_PATH)
#     with open(LABEL_PATH, "rb") as f: 
#         label_map = pickle.load(f)
    
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#     if not IS_CLOUD:
#         # ────────── PC MODE (LOCAL CAMERA) ──────────
#         cam = cv2.VideoCapture(0)
#         start = time.time()
#         best_conf = 999

#         while time.time() - start < 15:
#             ret, raw_frame = cam.read()
#             if not ret: break
            
#             frame = enhance_frame(raw_frame)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = detector.detectMultiScale(gray, 1.3, 5)
            
#             for (x, y, w, h) in faces:
#                 lab_id, conf = model.predict(gray[y:y+h, x:x+w])
#                 predicted_folder = label_map.get(lab_id)

#                 if predicted_folder == selected_user:
#                     if conf < 50:
#                         cam.release()
#                         cv2.destroyAllWindows()
#                         return True, conf
            
#             cv2.imshow("BioPay PC Scan", frame)
#             if cv2.waitKey(1) == 27: break
        
#         cam.release()
#         cv2.destroyAllWindows()
#         return False, 999

#     else:
#         # ────────── CLOUD/PHONE MODE (WEBRTC) ──────────
#         st.info("📸 Camera Active: Please position your face in the frame.")
        
#         # Webrtc configuration for mobile stability
#         RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

#         # This component opens the camera on the Phone/Browser
#         webrtc_ctx = webrtc_streamer(
#             key="face-auth",
#             mode=WebRtcMode.SENDRECV,
#             rtc_configuration=RTC_CONFIG,
#             media_stream_constraints={"video": True, "audio": False},
#             async_processing=True,
#         )

#         # In a web app, we use a manual trigger or a timer
#         if st.button("Click to Confirm Identity"):
#             if webrtc_ctx.video_receiver:
#                 # Get the latest frame from the phone
#                 frame = webrtc_ctx.video_receiver.get_frame()
#                 if frame:
#                     img = frame.to_ndarray(format="bgr24")
#                     img = enhance_frame(img)
#                     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                     faces = detector.detectMultiScale(gray, 1.3, 5)
                    
#                     for (x, y, w, h) in faces:
#                         lab_id, conf = model.predict(gray[y:y+h, x:x+w])
#                         if label_map.get(lab_id) == selected_user and conf < 70:
#                             st.success(f"Identity Verified! (Conf: {int(conf)})")
#                             return True, conf
#             st.error("Verification failed. Please try again.")
#             return False, 999

#     return False, 999

# import cv2
# import pickle
# import os
# import time
# import numpy as np
# import streamlit as st
# import av
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# # --- PATHING ---
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "model", "face_model.yml")
# LABEL_PATH = os.path.join(BASE_DIR, "model", "labels.pkl")

# def enhance_frame(frame):
#     img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
#     return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

# def authenticate(selected_user):
#     IS_CLOUD = os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud"
    
#     if not os.path.exists(MODEL_PATH):
#         st.error("Model missing!")
#         return False, 999

#     model = cv2.face.LBPHFaceRecognizer_create()
#     model.read(MODEL_PATH)
#     with open(LABEL_PATH, "rb") as f: label_map = pickle.load(f)
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#     if not IS_CLOUD:
#         # ────────── PC MODE ──────────
#         cam = cv2.VideoCapture(0)
#         start = time.time()
#         while time.time() - start < 15:
#             ret, raw = cam.read()
#             if not ret: break
#             frame = enhance_frame(raw)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = detector.detectMultiScale(gray, 1.3, 5)
#             for (x, y, w, h) in faces:
#                 lab_id, conf = model.predict(gray[y:y+h, x:x+w])
#                 if label_map.get(lab_id) == selected_user and conf < 50:
#                     cam.release(); cv2.destroyAllWindows()
#                     return True, conf
#             cv2.imshow("BioPay Scan", frame)
#             if cv2.waitKey(1) == 27: break
#         cam.release(); cv2.destroyAllWindows(); return False, 999

#     else:
#         # ────────── MOBILE MODE ──────────
#         st.warning("📸 Look at the camera and click Verify.")
#         ctx = webrtc_streamer(
#             key="face-mobile",
#             rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#             media_stream_constraints={"video": True, "audio": False}
#         )
#         if st.button("Verify Identity"):
#             if ctx.video_receiver:
#                 frame = ctx.video_receiver.get_frame()
#                 if frame:
#                     img = enhance_frame(frame.to_ndarray(format="bgr24"))
#                     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                     faces = detector.detectMultiScale(gray, 1.3, 5)
#                     for (x, y, w, h) in faces:
#                         lab_id, conf = model.predict(gray[y:y+h, x:x+w])
#                         if label_map.get(lab_id) == selected_user and conf < 75:
#                             return True, conf
#             st.error("Recognition Failed")
#             return False, 999
#     return False, 999

import cv2
import pickle
import os
import time
import numpy as np
import streamlit as st
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- PATHING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "face_model.yml")
LABEL_PATH = os.path.join(BASE_DIR, "model", "labels.pkl")


def enhance_frame(frame):
    img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)


def authenticate(selected_user):

    IS_CLOUD = os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud"

    if not os.path.exists(MODEL_PATH):
        st.error("Face model missing!")
        return False, 999

    model = cv2.face.LBPHFaceRecognizer_create()
    model.read(MODEL_PATH)

    with open(LABEL_PATH, "rb") as f:
        label_map = pickle.load(f)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    best_conf = 999

    # ─────────────────────────────
    # PC MODE
    # ─────────────────────────────
    if not IS_CLOUD:

        cam = cv2.VideoCapture(0)
        start = time.time()

        while time.time() - start < 15:

            ret, raw = cam.read()
            if not ret:
                break

            frame = enhance_frame(raw)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:

                lab_id, conf = model.predict(gray[y:y+h, x:x+w])
                predicted_user = label_map.get(lab_id)

                if predicted_user == selected_user:

                    if conf < best_conf:
                        best_conf = conf

                    if conf < 50:

                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        cv2.putText(frame,"Identity Verified",
                                    (x,y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,(0,255,0),2)

                        cam.release()
                        cv2.destroyAllWindows()
                        return True, conf

                    else:

                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                        cv2.putText(frame,"Match Weak - Move Closer",
                                    (x,y-10),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,(0,255,255),2)

                else:

                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                    cv2.putText(frame,"Unknown Identity",
                                (x,y-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,(0,0,255),2)

            cv2.imshow("BioPay Secure Scan", frame)

            if cv2.waitKey(1) == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        return False, best_conf


    # ─────────────────────────────
    # MOBILE / CLOUD MODE
    # ─────────────────────────────
    else:

        st.warning("📸 Look at the camera and press Verify")

        ctx = webrtc_streamer(
            key="face-mobile",
            rtc_configuration={
                "iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={"video":True,"audio":False}
        )

        if st.button("Verify Identity"):

            if ctx.video_receiver:

                frame = ctx.video_receiver.get_frame()

                if frame:

                    img = enhance_frame(frame.to_ndarray(format="bgr24"))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                    faces = detector.detectMultiScale(gray,1.3,5)

                    for (x,y,w,h) in faces:

                        lab_id, conf = model.predict(gray[y:y+h,x:x+w])
                        predicted_user = label_map.get(lab_id)

                        if predicted_user == selected_user:

                            if conf < best_conf:
                                best_conf = conf

                            if conf < 75:

                                st.success("✅ Identity Verified")
                                return True, conf

                            else:

                                st.warning("⚠ Weak Match - Move Closer")

                        else:

                            st.error("❌ Unknown Identity")

            st.error("Recognition Failed")
            return False, best_conf

    return False, best_conf