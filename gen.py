from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

# Génération
priv = ed25519.Ed25519PrivateKey.generate()
pub = priv.public_key()

# Sauvegarde Clé Privée (pour votre PC)
with open("private_key.pem", "wb") as f:
    f.write(priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Sauvegarde Clé Publique (pour le Robot Flex)
with open("public_key.pem", "wb") as f:
    f.write(pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Clés générées : private_key.pem et public_key.pem")