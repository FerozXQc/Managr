import os
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def verify_password_hash(plain_password:str,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def get_password_hash(plain_password:str):
    return password_hash.hash(plain_password)

