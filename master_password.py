import hasher
import secrets
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from pathlib import Path

#The length of the salt in bytes
SALT_LENGTH = 16
NONCE_LENGTH = 16
FILENAME = "password.txt"
value = ""

def exists():
    return Path(FILENAME).is_file()
    
def change(new_password):
    global value

    file = open(FILENAME, "w")
    new_password_hashed = hasher.hash(new_password)
    file.write(new_password_hashed)
    file.close()

    value = new_password

def verify(password):
    global value

    file = open(FILENAME, "r")
    password_hashed = file.read()
    is_valid = hasher.verify(password_hashed, password)
    file.close()

    #Rehash the password if outdated (?)
    if is_valid:
        value = password
        if hasher.needs_rehash(password_hashed):
            password_rehashed = hasher.hash(password)
            file = open(FILENAME, "w")
            file.write(password_rehashed)
            file.close()

    return is_valid

def encrypt(text):
    salt = secrets.token_bytes(SALT_LENGTH)
    hased_master_password = hasher.hash_raw(value, salt)
    
    aes = AES.new(hased_master_password, AES.MODE_EAX)
    nonce = aes.nonce
    encrypted_text = aes.encrypt(text.encode("utf-8"))

    return b64encode(salt + nonce + encrypted_text)

def decrypt(encoded_text):
    encoded_text = b64decode(encoded_text)

    salt = encoded_text[:SALT_LENGTH]
    nonce = encoded_text[SALT_LENGTH:SALT_LENGTH + NONCE_LENGTH]
    encrypted_text = encoded_text[SALT_LENGTH + NONCE_LENGTH - len(encoded_text):]
    hased_master_password = hasher.hash_raw(value, salt)

    aes = AES.new(hased_master_password, AES.MODE_EAX, nonce=nonce)
    text = aes.decrypt(encrypted_text).decode("utf-8")
    return text