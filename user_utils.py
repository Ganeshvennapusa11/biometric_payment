# import os
# import shutil
# import cv2
# import numpy as np
# import json
# import hashlib
# import threading
# from datetime import datetime
# from otp_utils import send_transaction_mail  # Ensure this function is in otp_utils.py

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATASET_DIR = os.path.join(BASE_DIR, "dataset")

# # -------------------------------------------------
# # NEW LOGIC: BLOCKCHAIN HASH GENERATOR
# # -------------------------------------------------
# def generate_block_hash(prev_hash, sender_id, receiver_id, amount, timestamp):
#     """Creates a unique SHA-256 signature for a transaction block."""
#     block_string = f"{prev_hash}{sender_id}{receiver_id}{amount}{timestamp}"
#     return hashlib.sha256(block_string.encode()).hexdigest()

# # -------------------------------------------------
# # GET ALL REGISTERED USERS
# # -------------------------------------------------
# def get_all_users():
#     if not os.path.exists("dataset"): return []
#     return [u for u in os.listdir("dataset") if os.path.isdir(f"dataset/{u}")]

# # -------------------------------------------------
# # READ USER METADATA
# # -------------------------------------------------
# def get_user_data(username):
#     path = f"dataset/{username}/user.json"
#     if not os.path.exists(path): return None
#     with open(path, "r") as f: return json.load(f)

# # -------------------------------------------------
# # DUAL-USER TRANSACTION LOGIC (WITH HASHING)
# # -------------------------------------------------
# def update_transaction(username, amount, receiver_id):
#     """
#     Subtracts money from sender, adds to receiver, 
#     generates a Blockchain Hash, and sends high-end HTML dual emails.
#     """
#     sender_path = f"dataset/{username}/user.json"
#     sender_data = get_user_data(username)
#     if not sender_data: return False

#     # 1. Check Sender Balance
#     curr_sender_bal = float(sender_data.get("balance", 0))
#     if curr_sender_bal < amount:
#         return False

#     # 2. Find Receiver Folder in Dataset
#     receiver_folder = None
#     receiver_data = None
#     for u in get_all_users():
#         temp_data = get_user_data(u)
#         if temp_data and temp_data.get("unique_id") == receiver_id:
#             receiver_folder = u
#             receiver_data = temp_data
#             break
    
#     if not receiver_data:
#         print("Receiver ID not found in system.")
#         return False

#     # --- BLOCKCHAIN LOGIC START ---
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     sender_history = sender_data.get("transactions", [])
#     prev_hash_sender = sender_history[-1]['hash'] if sender_history and 'hash' in sender_history[-1] else "00000000000000000000"
    
#     # Generate new unique hash
#     tx_hash = generate_block_hash(prev_hash_sender, sender_data.get("unique_id"), receiver_id, amount, timestamp)
#     # --- BLOCKCHAIN LOGIC END ---

#     # 3. Update Sender Balance & History
#     sender_data["balance"] = curr_sender_bal - amount
#     if "transactions" not in sender_data: sender_data["transactions"] = []
#     sender_data["transactions"].append({
#         "type": "Debit",
#         "to": receiver_id, 
#         "amount": amount,
#         "timestamp": timestamp,
#         "prev_hash": prev_hash_sender,
#         "hash": tx_hash,
#         "status": "Success"
#     })

#     # 4. Update Receiver Balance & History
#     curr_receiver_bal = float(receiver_data.get("balance", 0))
#     receiver_data["balance"] = curr_receiver_bal + amount
#     if "transactions" not in receiver_data: receiver_data["transactions"] = []
#     receiver_data["transactions"].append({
#         "type": "Credit",
#         "from": sender_data.get("unique_id"), 
#         "amount": amount,
#         "timestamp": timestamp,
#         "hash": tx_hash,
#         "status": "Success"
#     })

#     # 5. Save Both JSON Files
#     with open(sender_path, "w") as f: 
#         json.dump(sender_data, f, indent=4)
#     with open(f"dataset/{receiver_folder}/user.json", "w") as f: 
#         json.dump(receiver_data, f, indent=4)

#     # ---------------------------------------------------------
#     # 6. SEND DUAL EMAIL NOTIFICATIONS (PROFESSIONAL UI)
#     # ---------------------------------------------------------

#     # A. DEBIT EMAIL (RED THEME)
#     html_debit = f"""
#     <div style="font-family: sans-serif; padding: 25px; border: 1px solid #e2e8f0; border-radius: 15px; max-width: 600px; background-color: #ffffff;">
#         <div style="background-color: #fc8181; padding: 15px; border-radius: 10px 10px 0 0; text-align: center; color: white;">
#             <h2 style="margin:0; letter-spacing: 1px; text-transform: uppercase; font-size: 16px;">Debit Alert</h2>
#         </div>
#         <div style="background-color: #f7fafc; padding: 25px; border: 1px solid #edf2f7; border-top: none; border-radius: 0 0 12px 12px;">
#             <table style="width: 100%; border-collapse: collapse;">
#                 <tr><td style="padding: 10px 0; color: #718096;">Amount Debited</td><td style="text-align:right; color:#e53e3e; font-weight:bold; font-size: 1.4rem;">- ₹{amount:,}</td></tr>
#                 <tr><td style="padding: 10px 0; color: #718096;">Sent To</td><td style="text-align:right; font-weight: 500;">{receiver_id}</td></tr>
#                 <tr><td style="padding: 10px 0; color: #718096;">Blockchain Hash</td><td style="text-align:right; font-family:monospace; font-size: 0.75rem; color: #4a5568;">{tx_hash[:20]}...</td></tr>
#                 <tr><td style="padding: 15px 0 0 0; border-top: 1px solid #e2e8f0; color: #2d3748; font-weight:bold;">Remaining Balance</td><td style="text-align:right; padding: 15px 0 0 0; font-weight:bold; color: #2d3748;">₹{sender_data['balance']:,}</td></tr>
#             </table>
#         </div>
#         <p style="font-size: 0.75rem; color: #a0aec0; text-align: center; margin-top: 20px;">Verified via 🛡️ BioPay Biometric Identity Layer</p>
#     </div>
#     """

#     # B. CREDIT EMAIL (GREEN THEME)
#     html_credit = f"""
#     <div style="font-family: sans-serif; padding: 25px; border: 1px solid #e2e8f0; border-radius: 15px; max-width: 600px; background-color: #ffffff;">
#         <div style="background-color: #48bb78; padding: 15px; border-radius: 10px 10px 0 0; text-align: center; color: white;">
#             <h2 style="margin:0; letter-spacing: 1px; text-transform: uppercase; font-size: 16px;">Credit Alert</h2>
#         </div>
#         <div style="background-color: #f7fafc; padding: 25px; border: 1px solid #edf2f7; border-top: none; border-radius: 0 0 12px 12px;">
#             <table style="width: 100%; border-collapse: collapse;">
#                 <tr><td style="padding: 10px 0; color: #718096;">Amount Received</td><td style="text-align:right; color:#48bb78; font-weight:bold; font-size: 1.4rem;">+ ₹{amount:,}</td></tr>
#                 <tr><td style="padding: 10px 0; color: #718096;">From Sender</td><td style="text-align:right; font-weight: 500;">{sender_data.get('unique_id')}</td></tr>
#                 <tr><td style="padding: 10px 0; color: #718096;">Blockchain Hash</td><td style="text-align:right; font-family:monospace; font-size: 0.75rem; color: #4a5568;">{tx_hash[:20]}...</td></tr>
#                 <tr><td style="padding: 15px 0 0 0; border-top: 1px solid #e2e8f0; color: #2d3748; font-weight:bold;">Updated Balance</td><td style="text-align:right; padding: 15px 0 0 0; font-weight:bold; color: #2d3748;">₹{receiver_data['balance']:,}</td></tr>
#             </table>
#         </div>
#         <p style="font-size: 0.75rem; color: #a0aec0; text-align: center; margin-top: 20px;">Received via 🛡️ BioPay Secure Infrastructure</p>
#     </div>
#     """

#     # Send Mails
#     send_transaction_mail(sender_data['email'], "Debit Alert: BioPay Transaction Successful", html_debit)
#     send_transaction_mail(receiver_data['email'], "Credit Alert: BioPay Payment Received", html_credit)

#     return True
# # -------------------------------------------------
# # CHECK IF USER EXISTS
# # -------------------------------------------------
# def check_user_exists(email, name, mobile):
#     for u in get_all_users():
#         d = get_user_data(u)
#         if d:
#             if d.get('email') == email or d.get('mobile') == mobile: 
#                 return True, "User with this Email or Mobile already exists."
#     return False, ""

# # -------------------------------------------------
# # UPDATE FAILED ATTEMPTS
# # -------------------------------------------------
# def update_failed_attempts(username, success):
#     user_file = f"dataset/{username}/user.json"
#     if not os.path.exists(user_file): return

#     with open(user_file, "r") as f:
#         data = json.load(f)

#     if success:
#         data["failed_attempts"] = 0
#     else:
#         data["failed_attempts"] = data.get("failed_attempts", 0) + 1

#     with open(user_file, "w") as f:
#         json.dump(data, f, indent=4)

# # -------------------------------------------------
# # PHOTO & PROFILE MANAGEMENT
# # -------------------------------------------------
# def update_profile_photo(username, uploaded_file):
#     path = f"dataset/{username}/profile.jpg"
#     file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#     img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#     if img is not None:
#         cv2.imwrite(path, img)

# def delete_user(username):
#     path = f"dataset/{username}"
#     if os.path.exists(path):
#         shutil.rmtree(path)

# def rename_user(old_name, new_name):
#     old_path = f"dataset/{old_name}"
#     new_path = f"dataset/{new_name}"
#     if not os.path.exists(old_path) or os.path.exists(new_path):
#         return False
#     os.rename(old_path, new_path)
#     return True

# def update_user_balance(target_email, new_balance):
#     if not os.path.exists(DATASET_DIR):
#         return False
#     #base_path = r"G:\biometric_payment_system\dataset"
    
#     # 1. Look through EVERY folder in the dataset
#     # for folder_name in os.listdir(base_path):
#     for folder_name in os.listdir(DATASET_DIR):
#         #json_path = os.path.join(base_path, folder_name, "profile.json")
#         json_path = os.path.join(DATASET_DIR, folder_name, "user.json")
        
#         if os.path.exists(json_path):
#             try:
#                 with open(json_path, 'r') as f:
#                     data = json.load(f)
                
#                 # 2. Check if the email inside THIS file matches the user we want to fine
#                 if data.get('email') == target_email:
#                     data['balance'] = new_balance
#                     with open(json_path, 'w') as f:
#                         json.dump(data, f, indent=4)
#                     return True # FOUND AND UPDATED
#             except:
#                 continue
                
#     return False # Truly not found anywhere

import os
import shutil
import cv2
import numpy as np
import json
import hashlib
import threading
from datetime import datetime
from otp_utils import send_transaction_mail


# --- DYNAMIC PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

# Ensure dataset directory exists
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# -------------------------------------------------
# BLOCKCHAIN HASH GENERATOR
# -------------------------------------------------
def generate_block_hash(prev_hash, sender_id, receiver_id, amount, timestamp):
    block_string = f"{prev_hash}{sender_id}{receiver_id}{amount}{timestamp}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# -------------------------------------------------
# GET ALL REGISTERED USERS
# -------------------------------------------------
def get_all_users():
    if not os.path.exists(DATASET_DIR): return []
    return [u for u in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, u))]

# -------------------------------------------------
# READ USER METADATA
# -------------------------------------------------
def get_user_data(username):
    path = os.path.join(DATASET_DIR, username, "user.json")
    if not os.path.exists(path): return None
    with open(path, "r") as f: return json.load(f)

# -------------------------------------------------
# TRANSACTION LOGIC
# -------------------------------------------------
def update_transaction(username, amount, receiver_id):
    sender_path = os.path.join(DATASET_DIR, username, "user.json")
    sender_data = get_user_data(username)
    if not sender_data: return False

    # 1. Check Sender Balance
    curr_sender_bal = float(sender_data.get("balance", 0))
    if curr_sender_bal < amount:
        return False

    # 2. Find Receiver
    receiver_folder = None
    receiver_data = None
    for u in get_all_users():
        temp_data = get_user_data(u)
        if temp_data and temp_data.get("unique_id") == receiver_id:
            receiver_folder = u
            receiver_data = temp_data
            break
    
    if not receiver_data: return False

    # --- BLOCKCHAIN LOGIC ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sender_history = sender_data.get("transactions", [])
    prev_hash_sender = sender_history[-1]['hash'] if sender_history and 'hash' in sender_history[-1] else "0" * 64
    tx_hash = generate_block_hash(prev_hash_sender, sender_data.get("unique_id"), receiver_id, amount, timestamp)

    # 3. Update Sender
    sender_data["balance"] = curr_sender_bal - amount
    if "transactions" not in sender_data: sender_data["transactions"] = []
    sender_data["transactions"].append({
        "type": "Debit", "to": receiver_id, "amount": amount,
        "timestamp": timestamp, "hash": tx_hash, "status": "Success"
    })

    # 4. Update Receiver
    receiver_data["balance"] = float(receiver_data.get("balance", 0)) + amount
    if "transactions" not in receiver_data: receiver_data["transactions"] = []
    receiver_data["transactions"].append({
        "type": "Credit", "from": sender_data.get("unique_id"), "amount": amount,
        "timestamp": timestamp, "hash": tx_hash, "status": "Success"
    })

    # 5. Save Files
    with open(sender_path, "w") as f: json.dump(sender_data, f, indent=4)
    with open(os.path.join(DATASET_DIR, receiver_folder, "user.json"), "w") as f: 
        json.dump(receiver_data, f, indent=4)

    # ---------------------------------------------------------
    # 6. HTML TEMPLATES (THE FIX IS HERE)
    # ---------------------------------------------------------
    html_debit = f"""
    <div style="font-family: sans-serif; padding: 25px; border: 1px solid #e2e8f0; border-radius: 15px; max-width: 600px; background-color: #ffffff;">
        <div style="background-color: #fc8181; padding: 15px; border-radius: 10px 10px 0 0; text-align: center; color: white;">
            <h2 style="margin:0; letter-spacing: 1px; text-transform: uppercase; font-size: 16px;">Debit Alert</h2>
        </div>
        <div style="background-color: #f7fafc; padding: 25px; border: 1px solid #edf2f7; border-top: none; border-radius: 0 0 12px 12px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 10px 0; color: #718096;">Amount Debited</td><td style="text-align:right; color:#e53e3e; font-weight:bold; font-size: 1.4rem;">- ₹{amount:,}</td></tr>
                <tr><td style="padding: 10px 0; color: #718096;">Sent To</td><td style="text-align:right; font-weight: 500;">{receiver_id}</td></tr>
                <tr><td style="padding: 10px 0; color: #718096;">Blockchain Hash</td><td style="text-align:right; font-family:monospace; font-size: 0.75rem; color: #4a5568;">{tx_hash[:20]}...</td></tr>
                <tr><td style="padding: 15px 0 0 0; border-top: 1px solid #e2e8f0; color: #2d3748; font-weight:bold;">Remaining Balance</td><td style="text-align:right; padding: 15px 0 0 0; font-weight:bold; color: #2d3748;">₹{sender_data['balance']:,}</td></tr>
            </table>
        </div>
        <p style="font-size: 0.75rem; color: #a0aec0; text-align: center; margin-top: 20px;">Verified via 🛡️ BioPay Biometric Identity Layer</p>
    </div>
    """

    # B. CREDIT EMAIL (GREEN THEME)
    html_credit = f"""
    <div style="font-family: sans-serif; padding: 25px; border: 1px solid #e2e8f0; border-radius: 15px; max-width: 600px; background-color: #ffffff;">
        <div style="background-color: #48bb78; padding: 15px; border-radius: 10px 10px 0 0; text-align: center; color: white;">
            <h2 style="margin:0; letter-spacing: 1px; text-transform: uppercase; font-size: 16px;">Credit Alert</h2>
        </div>
        <div style="background-color: #f7fafc; padding: 25px; border: 1px solid #edf2f7; border-top: none; border-radius: 0 0 12px 12px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 10px 0; color: #718096;">Amount Received</td><td style="text-align:right; color:#48bb78; font-weight:bold; font-size: 1.4rem;">+ ₹{amount:,}</td></tr>
                <tr><td style="padding: 10px 0; color: #718096;">From Sender</td><td style="text-align:right; font-weight: 500;">{sender_data.get('unique_id')}</td></tr>
                <tr><td style="padding: 10px 0; color: #718096;">Blockchain Hash</td><td style="text-align:right; font-family:monospace; font-size: 0.75rem; color: #4a5568;">{tx_hash[:20]}...</td></tr>
                <tr><td style="padding: 15px 0 0 0; border-top: 1px solid #e2e8f0; color: #2d3748; font-weight:bold;">Updated Balance</td><td style="text-align:right; padding: 15px 0 0 0; font-weight:bold; color: #2d3748;">₹{receiver_data['balance']:,}</td></tr>
            </table>
        </div>
        <p style="font-size: 0.75rem; color: #a0aec0; text-align: center; margin-top: 20px;">Received via 🛡️ BioPay Secure Infrastructure</p>
    </div>
    """

    # Send Mails
    try:
        send_transaction_mail(sender_data['email'], "Debit Alert: BioPay Success", html_debit)
        send_transaction_mail(receiver_data['email'], "Credit Alert: BioPay Success", html_credit)
    except Exception as e:
        print(f"Mail Error: {e}")

    return True
# -------------------------------------------------
# PROFILE & UTILITIES
# -------------------------------------------------
def check_user_exists(email, name, mobile):
    for u in get_all_users():
        d = get_user_data(u)
        if d and (d.get('email') == email or d.get('mobile') == mobile): 
            return True, "User with this Email or Mobile already exists."
    return False, ""

def update_failed_attempts(username, success):
    user_file = os.path.join(DATASET_DIR, username, "user.json")
    data = get_user_data(username)
    if not data: return

    data["failed_attempts"] = 0 if success else data.get("failed_attempts", 0) + 1
    with open(user_file, "w") as f: json.dump(data, f, indent=4)

def update_profile_photo(username, uploaded_file):
    path = os.path.join(DATASET_DIR, username, "profile.jpg")
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is not None: cv2.imwrite(path, img)

def delete_user(username):
    path = os.path.join(DATASET_DIR, username)
    if os.path.exists(path): shutil.rmtree(path)

def update_user_balance(target_email, new_balance):
    for folder_name in os.listdir(DATASET_DIR):
        json_path = os.path.join(DATASET_DIR, folder_name, "user.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f: data = json.load(f)
                if data.get('email') == target_email:
                    data['balance'] = new_balance
                    with open(json_path, 'w') as f: json.dump(data, f, indent=4)
                    return True
            except: continue
    return False

def rename_user(old_name, new_name):
    """Renames a user folder while maintaining path compatibility."""
    old_path = os.path.join(DATASET_DIR, old_name)
    new_path = os.path.join(DATASET_DIR, new_name)
    
    if not os.path.exists(old_path) or os.path.exists(new_path):
        return False
        
    try:
        os.rename(old_path, new_path)
        return True
    except Exception as e:
        print(f"Rename error: {e}")
        return False
    
# ─── PIN UTILITIES (append these to your existing user_utils.py) ──────────────
#
# Add the two functions below to the bottom of your user_utils.py file.
# No existing functions need to be changed.
# ──────────────────────────────────────────────────────────────────────────────

import hashlib


def verify_user_pin(sender_folder: str, entered_pin: str) -> bool:
    """
    Verify a 4-digit PIN against the stored SHA-256 hash.

    Parameters
    ----------
    sender_folder : str
        The folder key for the user (email with @ and . replaced by _).
    entered_pin : str
        The plain-text PIN the user typed in the UI.

    Returns
    -------
    bool  True if PIN matches, False otherwise.
    """
    import json, os
    user_file = f"dataset/{sender_folder}/user.json"
    if not os.path.exists(user_file):
        return False

    with open(user_file, "r") as f:
        data = json.load(f)

    stored_hash = data.get("personal_pin_hash", "")
    if not stored_hash:
        # User registered before PIN feature was added — treat as no PIN set
        return False

    entered_hash = hashlib.sha256(entered_pin.encode()).hexdigest()
    return entered_hash == stored_hash


def has_pin_registered(sender_folder: str) -> bool:
    """Return True if the user has a PIN hash stored."""
    import json, os
    user_file = f"dataset/{sender_folder}/user.json"
    if not os.path.exists(user_file):
        return False
    with open(user_file, "r") as f:
        data = json.load(f)
    return bool(data.get("personal_pin_hash", ""))