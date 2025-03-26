## @package utils.crypt_utils
# Cryptography utility functions
#
# This module provides utility functions for RSA key generation and encryption/decryption of private keys.
#
# It uses the PyCryptodome library for cryptographic operations.

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

## Length of the RSA key
RSA_KEY_LENGTH = 4096


## Generate RSA key pair
# @return Tuple of private key and public key in bytes
def generate_rsa_keys():
    key = RSA.generate(RSA_KEY_LENGTH)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

## Encrypt the private key using a PIN
# @param private_key Private key in bytes
# @param pin PIN to encrypt the private key
# @return Encrypted private key in bytes
def encrypt_private_key(private_key: bytes, pin: str):
    hash_obj = SHA256.new(pin.encode('utf-8'))
    aes_key = hash_obj.digest()
    
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(private_key)
    
    return cipher.nonce + tag + ciphertext

## Decrypt the private key using a PIN
# @param encrypted_key Encrypted private key in bytes
# @param pin PIN to decrypt the private key
# @return Decrypted private key as RSA key object
def decrypt_private_key(encrypted_key: bytes, pin: str):
    hash_obj = SHA256.new(pin.encode('utf-8'))
    aes_key = hash_obj.digest()
    
    nonce, tag, ciphertext = encrypted_key[:16], encrypted_key[16:32], encrypted_key[32:]
    cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
    
    try:
        private_key = cipher.decrypt_and_verify(ciphertext, tag)
        return RSA.import_key(private_key)
    except ValueError:
        return None
