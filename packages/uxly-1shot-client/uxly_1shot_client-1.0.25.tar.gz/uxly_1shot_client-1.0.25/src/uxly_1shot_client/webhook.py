"""Webhook verification utilities for the 1Shot API."""

import base64
import json
from typing import Dict, Any, Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature


def verify_webhook(
    body: Dict[str, Any],
    signature: str,
    public_key: str,
) -> bool:
    """Verify a webhook signature.

    Args:
        body: The webhook request body
        signature: The webhook signature
        public_key: The base64-encoded public key

    Returns:
        True if the signature is valid, False otherwise

    Raises:
        ValueError: If the public key is invalid
        InvalidSignature: If the signature is invalid
    """
    try:
        # Create a copy of the body and remove the signature
        body_copy = body.copy()
        body_copy.pop("signature", None)

        # Decode the public key and signature
        public_key_bytes = base64.b64decode(public_key)
        signature_bytes = base64.b64decode(signature)

        # Create the public key object
        ed25519_public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

        # Verify the signature
        message = json.dumps(body_copy, separators=(',', ':'), sort_keys=True).encode('utf-8')
        ed25519_public_key.verify(signature_bytes, message)
        return True
    except (ValueError, InvalidSignature) as e:
        raise e
    except Exception as e:
        raise ValueError(f"Error verifying webhook signature: {str(e)}")


class WebhookVerifier:
    """A class for verifying webhook signatures."""

    def __init__(self, public_key: str):
        """Initialize the webhook verifier.

        Args:
            public_key: The base64-encoded public key

        Raises:
            ValueError: If the public key is invalid
        """
        try:
            self.public_key = public_key
            # Validate the public key by attempting to decode it
            base64.b64decode(public_key)
        except Exception as e:
            raise ValueError(f"Invalid public key: {str(e)}")

    def verify(self, body: Dict[str, Any], signature: str) -> bool:
        """Verify a webhook signature.

        Args:
            body: The webhook request body
            signature: The webhook signature

        Returns:
            True if the signature is valid, False otherwise

        Raises:
            ValueError: If the public key is invalid
            InvalidSignature: If the signature is invalid
        """
        return verify_webhook(body, signature, self.public_key) 
    