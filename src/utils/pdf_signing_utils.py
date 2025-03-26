## @package utils.pdf_signing_utils
# PDF signing utility functions
#
# This module provides utility functions for signing and verifying PDF files using RSA digital signatures.

from Crypto.PublicKey import RSA
import hashlib

## Length of the RSA signature in bytes
SIGNATURE_LENGTH = 512

## Length of the hash in bytes
HASH_LENGTH = 256


## Sign a PDF file using an RSA private key
# @param pdf_path Path of the PDF file to sign
# @param private_key RSA private key object
# @param signed_pdf_path Path to save the signed PDF file
# @return Path of the signed PDF file
def sign_pdf(pdf_path: str, private_key: RSA.RsaKey, signed_pdf_path: str | None = None):
    if signed_pdf_path is None:
        signed_pdf_path = pdf_path.replace('.pdf', '_signed.pdf')

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    pdf_hash = hashlib.sha256(pdf_data).digest()

    signature = pow(int.from_bytes(pdf_hash, byteorder='big'), private_key.d, private_key.n)
    signature_bytes = signature.to_bytes(SIGNATURE_LENGTH, byteorder='big')

    with open(signed_pdf_path, 'wb') as f:
        f.write(pdf_data + signature_bytes)

    return signed_pdf_path

## Verify the signature of a signed PDF file using an RSA public key
# @param pdf_path Path of the signed PDF file
# @param public_key RSA public key object
# @return True if the signature is valid, False otherwise
def verify_signature(pdf_path: str, public_key: RSA.RsaKey):
    with open(pdf_path, 'rb') as f:
        content = f.read()
    pdf_data, signature = content[:-SIGNATURE_LENGTH], content[-SIGNATURE_LENGTH:]
    pdf_hash = hashlib.sha256(pdf_data).digest()

    decrypted_hash = pow(int.from_bytes(signature, byteorder='big'), public_key.e, public_key.n)

    try:
        decrypted_hash_bytes = decrypted_hash.to_bytes(HASH_LENGTH//8, byteorder='big')
    except OverflowError:
        return False

    return pdf_hash == decrypted_hash_bytes
