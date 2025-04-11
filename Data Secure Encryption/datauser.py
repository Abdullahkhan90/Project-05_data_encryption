import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

# File and Security Settings
DATA_FILE = "secure_data.json"
SALT = b"secure_salt_value"
LOCKOUT_DURATION = 60  # seconds

# Initialize Session State
if "authenticated_user" not in st.session_state:
    st.session_state.authenticated_user = None
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0

# Load & Save Data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Hash & Encryption Functions
def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()

def generate_key(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)
    return urlsafe_b64encode(key)

def encrypt_text(text, passkey):
    cipher = Fernet(generate_key(passkey))
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, passkey):
    try:
        cipher = Fernet(generate_key(passkey))
        return cipher.decrypt(encrypted_text.encode()).decode()
    except:
        return None

stored_data = load_data()

# Streamlit UI
st.title("🔐 Abdullah Naeem Secure Data Encryption System")

menu = ["Home", "Register", "Login", "Store Data", "Retrieve Data"]
choice = st.sidebar.selectbox("Navigation", menu)

# Home Section
if choice == "Home":
    st.subheader("Welcome To The Secure Data Encryption System!")
    st.markdown("""
    - Encrypt Your Sensitive Data Safely.
    - Only Decrypt With Correct Passkey.
    - Multiple Failed Attempts = Temporary Lockout.
    """)

# Register Section
elif choice == "Register":
    st.subheader("Register New User")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")

    if st.button("Register"):
        if username and password:
            if username in stored_data:
                st.warning("⚠ User Already Exists.")
            else:
                stored_data[username] = {
                    "password": hash_password(password),
                    "data": []
                }
                save_data(stored_data)
                st.success("🎉 User Registered Successfully!")
        else:
            st.error("Both Fields Are Required!")

# Login Section
elif choice == "Login":
    if time.time() < st.session_state.lockout_time:
        remaining = int(st.session_state.lockout_time - time.time())
        st.error(f"Too Many Failed Attempts! Please wait {remaining} seconds.")
        st.stop()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in stored_data and stored_data[username]["password"] == hash_password(password):
            st.session_state.authenticated_user = username
            st.session_state.failed_attempts = 0
            st.success(f"😊 Welcome {username}!")
        else:
            st.session_state.failed_attempts += 1
            remaining = 3 - st.session_state.failed_attempts
            st.error(f"❌ Invalid Credentials! Attempts left: {remaining}")

            if st.session_state.failed_attempts >= 3:
                st.session_state.lockout_time = time.time() + LOCKOUT_DURATION
                st.error("Account Locked for 60 seconds!")
                st.stop()

# Store Data Section
elif choice == "Store Data":
    if not st.session_state.authenticated_user:
        st.warning("Please Login First!")
    else:
        st.subheader("Store Encrypted Data")
        data = st.text_area("Enter Data To Encrypt")
        passkey = st.text_input("Encryption Key (Passphrase)", type="password")

        if st.button("Encrypt & Save"):
            if data and passkey:
                encrypted = encrypt_text(data, passkey)
                stored_data[st.session_state.authenticated_user]["data"].append(encrypted)
                save_data(stored_data)
                st.success("✅ Data Encrypted & Saved Successfully!")
            else:
                st.error("All Fields Are Required!")

# Retrieve Data Section
elif choice == "Retrieve Data":
    if not st.session_state.authenticated_user:
        st.warning("Please Login First!")
    else:
        st.subheader("Retrieve & Decrypt Data")

        user_data = stored_data.get(st.session_state.authenticated_user, {}).get("data", [])

        if not user_data:
            st.info("No Data Found!")
        else:
            st.write("Your Encrypted Data:")
            for item in user_data:
                st.code(item, language="text")

            encrypted_input = st.text_area("Paste Encrypted Text")
            passkey = st.text_input("Enter Passkey To Decrypt", type="password")

            if st.button("Decrypt"):
                result = decrypt_text(encrypted_input, passkey)
                if result:
                    st.success(f"Decrypted Data: {result}")
                else:
                    st.error("❌ Incorrect Passkey or Corrupted Data!")
