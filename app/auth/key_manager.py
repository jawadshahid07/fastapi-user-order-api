import os
from cryptography.hazmat.primitives import serialization

# Load Private Key (for signing JWTs)
with open(".ssh/jwtRS256", "rb") as key_file:
    PRIVATE_KEY = serialization.load_pem_private_key(key_file.read(), password=None)

# Load Public Key (for verifying JWTs)
with open(".ssh/jwtRS256.pem", "rb") as key_file:
    PUBLIC_KEY = serialization.load_pem_public_key(key_file.read())
