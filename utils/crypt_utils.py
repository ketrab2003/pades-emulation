from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

RSA_KEY_LENGTH = 4096


def generate_rsa_keys():
    key = RSA.generate(RSA_KEY_LENGTH)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_private_key(private_key: bytes, pin: str):
    hash_obj = SHA256.new(pin.encode('utf-8'))
    aes_key = hash_obj.digest()
    
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(private_key)
    
    return cipher.nonce + tag + ciphertext

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
