## 🛡️ Python Assignment: Secure Data Encryption System Using Streamlit
Objective
Develop a Streamlit-based secure data storage and retrieval system where:

## Users store data with a unique passkey.
Users decrypt data by providing the correct passkey.
Multiple failed attempts result in a forced reauthorization (login page).
The system operates entirely in memory without external databases.
## 🔹 Requirements
1. Data Storage (In-Memory Dictionary)
Each entry is stored as:
stored_data = {
    "user1_data": {"encrypted_text": "some_ciphertext", "passkey": "hashed_passkey"},
    ...
}
Passkeys must be hashed (e.g., SHA-256).
2. Secure Encryption & Decryption
Encrypt data using Caesar cipher or Fernet (from cryptography library).
Decrypt only when the correct passkey is provided.
3. Authentication & Security
Allow three attempts before forcing a reauthorization/login page.
Display failed attempts count.
4. Streamlit UI (User-Friendly Interface)
Home Page: Options to store new data or retrieve data.
Insert Data Page:
User enters text + passkey, and it’s stored securely.
Retrieve Data Page:
User provides a passkey to decrypt data.
If failed 3 times, redirect to the Login Page for reauthorization.
Login Page: Simple login mechanism before retrying.
