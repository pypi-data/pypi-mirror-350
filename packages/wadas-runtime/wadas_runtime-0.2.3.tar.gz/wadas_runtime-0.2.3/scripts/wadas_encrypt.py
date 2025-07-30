"""Encrypts a file using AES-GCM encryption with a key derived from the hardware fingerprint."""

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import hwid
import os


def get_hardware_fingerprint() -> str:
    """
    Retrieve the hardware fingerprint of the current machine and hash it.

    This function utilizes the `hwid` module to obtain a unique hardware
    identifier (HWID) for the machine on which it is executed, then hashes it
    using SHA256 to generate a secure fingerprint.

    Returns:
        str: A string representing the hashed hardware fingerprint.
    """
    hwid_value = hwid.get_hwid()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(hwid_value.encode())
    hashed_fingerprint = digest.finalize().hex()
    return hashed_fingerprint


def derive_key_from_hw_fingerprint(
    fingerprint: str, salt: bytes = b"static-salt"
) -> bytes:
    """
    Derive a cryptographic key from a hardware fingerprint using PBKDF2.

    Args:
        fingerprint (str): The hardware fingerprint to derive the key from.
                           This is an unique identifier for the hardware.
        salt (bytes, optional): A salt value to use in the key derivation function.
                                Defaults to b"static-salt". Using a static salt ensures
                                deterministic key derivation.

    Returns:
        bytes: A 256-bit (32-byte) cryptographic key derived from the fingerprint and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit AES key
        salt=salt,  # Use a static salt for full determinism
        iterations=100_000,
        backend=default_backend(),
    )
    return kdf.derive(fingerprint.encode())


def encrypt_model(input_file: str, output_file: str) -> bytes:
    """Encrypt a file using AES-GCM encryption.

    Args:
        input_file (str): The path to the input file to be encrypted.
        output_file (str): The path to the output file where the encrypted content will be saved.
    Returns:
        bytes: The encryption key derived from the hardware fingerprint.
    Notes:
        - The encryption process uses a hardware fingerprint to derive the encryption key.
        - A 96-bit nonce is generated randomly and prefixed to the ciphertext for
          decryption purposes.
        - The encrypted file contains both the nonce and the ciphertext.
    """
    hw_fingerprint = get_hardware_fingerprint()

    key = derive_key_from_hw_fingerprint(hw_fingerprint)

    with open(input_file, "rb") as f:
        buffer = f.read()

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce
    ciphertext = aesgcm.encrypt(nonce, buffer, None)
    encrypted = nonce + ciphertext  # prefix nonce for decryption

    # Add encryption header
    header = b"WADAS_ENCRYPTED"
    encrypted_with_header = header + encrypted

    with open(output_file, "wb") as f:
        f.write(encrypted_with_header)

    return key
