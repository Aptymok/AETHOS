from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

out_dir = os.path.join(os.path.dirname(__file__), '..', '_secrets_staging')
if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)

priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
priv_pem = priv.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
pub = priv.public_key()
pub_pem = pub.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

priv_path = os.path.join(out_dir, 'dev_jwt_private.pem')
pub_path = os.path.join(out_dir, 'dev_jwt_public.pem')
with open(priv_path, 'wb') as f:
    f.write(priv_pem)
with open(pub_path, 'wb') as f:
    f.write(pub_pem)

print('Dev RSA keypair generated (private+public) in _secrets_staging (not printed).')
