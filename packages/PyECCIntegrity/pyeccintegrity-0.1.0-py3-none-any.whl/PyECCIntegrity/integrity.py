from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import base64

class ECCIntegrity:
    def __init__(self):
        """Generate ECC key pair for signing & verifying messages."""
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def sign_message(self, message: bytes) -> bytes:
        """Generate a digital signature using ECDSA (ECC)."""
        signature = self.private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256())  # Use SHA-256 for hashing
        )
        return signature

    def verify_signature(self, message: bytes, signature: bytes, sender_public_key_bytes: bytes) -> bool:
        """Verify the ECC digital signature for integrity check."""
        try:
            sender_public_key = serialization.load_pem_public_key(sender_public_key_bytes)
            sender_public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            return True  # ✅ Integrity Verified
        except InvalidSignature:
            return False  # ❌ Integrity Check Failed

    def export_public_key(self) -> bytes:
        """Export the public key (to share with receiver)."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

# Example Usage

def main():
    import base64
    sender = ECCIntegrity()
    message = b"Confidential Data Integrity Check"
    signature = sender.sign_message(message)
    public_key_bytes = sender.export_public_key()
    print(f"Message: {message.decode()}")
    print(f"Signature (Base64): {base64.b64encode(signature).decode()}")
    print(f"Sender Public Key:\n{public_key_bytes.decode()}")
    receiver = ECCIntegrity()
    if receiver.verify_signature(message, signature, public_key_bytes):
        print("✅ Integrity Verified: The message is authentic.")
    else:
        print("❌ Integrity Check Failed! Message may have been tampered.")
