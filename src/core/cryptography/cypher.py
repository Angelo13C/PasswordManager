from ..cryptography import hasher
import secrets
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

SALT_LENGTH = 16
NONCE_LENGTH = 16

def derive_key(key):
    salt = secrets.token_bytes(SALT_LENGTH)
    return derive_key(key, salt), salt

def derive_key(key, salt):
    return hasher.hash_raw(key, salt)

def encrypt(text, key):
    derived_key, salt = derive_key(key)
    
    aes = AES.new(derived_key, AES.MODE_EAX)
    nonce = aes.nonce
    encrypted_text = aes.encrypt(text.encode("utf-8"))

    return b64encode(salt + nonce + encrypted_text)

def decrypt(encoded_text, key):
    encoded_text = b64decode(encoded_text)

    salt = encoded_text[:SALT_LENGTH]
    nonce = encoded_text[SALT_LENGTH:SALT_LENGTH + NONCE_LENGTH]
    encrypted_text = encoded_text[SALT_LENGTH + NONCE_LENGTH - len(encoded_text):]
    derived_key = derive_key(key, salt)

    aes = AES.new(derived_key, AES.MODE_EAX, nonce=nonce)
    text = aes.decrypt(encrypted_text).decode("utf-8")
    return text