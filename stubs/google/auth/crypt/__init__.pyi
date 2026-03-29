from collections.abc import Sequence

from google.auth.crypt import base, es, es256, rsa

EsSigner = es.EsSigner
EsVerifier = es.EsVerifier
ES256Signer = es256.ES256Signer
ES256Verifier = es256.ES256Verifier
Signer = base.Signer
Verifier = base.Verifier
RSASigner = rsa.RSASigner
RSAVerifier = rsa.RSAVerifier

def verify_signature(
    message: str | bytes,
    signature: str | bytes,
    certs: Sequence[str | bytes] | str | bytes,
    verifier_cls: type[Verifier] = ...,
) -> bool: ...

__all__ = [
    "EsSigner",
    "EsVerifier",
    "ES256Signer",
    "ES256Verifier",
    "RSASigner",
    "RSAVerifier",
    "Signer",
    "Verifier",
]
