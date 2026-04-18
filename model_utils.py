import cv2, os, numpy as np, pickle

def train_model():
    faces, labels, label_map, l_id = [], [], {}, 0
    if not os.path.exists("dataset"): return False

    for user in os.listdir("dataset"):
        path = f"dataset/{user}"
        if not os.path.isdir(path): continue
        
        user_faces_count = 0
        for img in os.listdir(path):
            if img.startswith("face_"):
                img_data = cv2.imread(f"{path}/{img}", 0)
                if img_data is not None:
                    faces.append(img_data)
                    labels.append(l_id)
                    user_faces_count += 1
        
        if user_faces_count > 0:
            # Strictly map the integer ID to the folder name
            label_map[l_id] = user 
            l_id += 1

    if len(faces) < 2: return False

    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, np.array(labels))
    os.makedirs("model", exist_ok=True)
    model.save("model/face_model.yml")
    
    # Save mapping for targeted authentication
    with open("model/labels.pkl", "wb") as f: 
        pickle.dump(label_map, f)
    return True