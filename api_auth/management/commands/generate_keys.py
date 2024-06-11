import json
import os
from base64 import urlsafe_b64encode
from hashlib import sha256

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.conf import settings
from django.core.management.base import BaseCommand


def int_to_base64url(value):
    """Convert integer value to base64 URL-safe string without padding."""
    return (
        urlsafe_b64encode(value.to_bytes((value.bit_length() + 7) // 8, "big"))
        .decode("utf-8")
        .rstrip("=")
    )


def generate_key_pair_and_jwks(key_use):
    """Generate an RSA key pair and return the key and JWKS data."""
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()

    exponent = int_to_base64url(public_numbers.e)
    modulus = int_to_base64url(public_numbers.n)
    kid = sha256(f"{modulus}{exponent}{key_use}".encode("utf-8")).hexdigest()

    jwks_key = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "n": modulus,
        "e": exponent,
        "kid": kid,
    }

    return private_key, jwks_key


def save_key(private_key, path):
    """Save the RSA private key to a file."""
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


class Command(BaseCommand):
    help = 'Generates RSA keys for "generate" and "ingest" and combines them in a single JWKS file.'

    def handle(self, *args, **kwargs):
        jwks = {"keys": []}

        # for key_use in ['generate', 'ingest', 'external_test']:
        for key_use in ["external_test"]:
            private_key, jwks_key = generate_key_pair_and_jwks(key_use)

            # Save the private key
            private_key_path = os.path.join(
                settings.KEYS_DIR, f"private_key_{key_use}.pem"
            )
            save_key(private_key, private_key_path)

            # Add the JWKS key data
            jwks["keys"].append(jwks_key)

        # Save the combined JWKS to a file
        jwks_path = os.path.join(settings.KEYS_DIR, "jwks.json")
        with open(jwks_path, "w") as f:
            json.dump(jwks, f, indent=4)

        self.stdout.write(
            self.style.SUCCESS("Combined JWKS file generated successfully.")
        )
