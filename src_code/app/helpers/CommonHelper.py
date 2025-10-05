import hashlib
import os,re
import base64
import json
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import pytz
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from app.config.config import settings
import random
import time
from app.libraries.Logger import Logger
from app.helpers.ErrorCodes import ErrorCodes
from app.helpers.ErrorMessages import ErrorMessages
from app.config.CommonConstants import CommonConstants

logger = Logger.get_instance()
class CommonHelper :

    def __init__(self):
        self.ist = pytz.timezone('Asia/Kolkata')
        self.utf8 = 'utf-8'
        self.date_time_format = "%Y-%m-%d %H:%M:%S"

    
    def unix_timestamp(self):
        return int(datetime.now().timestamp())
    
    # Updated AES Encryption function using GCM mode
    def encrypt_aes(self, plaintext) -> str:
        encryptor_key = bytes.fromhex(settings.API_ENCRYPTION_KEY)
        iv = os.urandom(12)  # GCM mode requires a 12-byte IV
        cipher = Cipher(algorithms.AES(encryptor_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        # Include the IV and tag with the ciphertext
        return b64encode(iv + encryptor.tag + ciphertext).decode()

    # AES Decryption function using GCM mode
    def decrypt_aes(self, encrypted_data) -> str:
        encrypted_data = b64decode(encrypted_data)
        iv = encrypted_data[:12]  # Extract the 12-byte IV
        tag = encrypted_data[12:28]  # Extract the 16-byte GCM tag
        ciphertext = encrypted_data[28:]
        encryptor_key = bytes.fromhex(settings.API_ENCRYPTION_KEY)
        cipher = Cipher(algorithms.AES(encryptor_key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()


CommonClass = CommonHelper()
