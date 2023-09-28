import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.asymmetric import dh

# Configurações do socket
host = '127.0.0.1'
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    # Receber chave pública Diffie-Hellman de Alice
    serialized_public = s.recv(1024)
    alice_public_key_dh = serialization.load_pem_public_key(serialized_public, backend=default_backend())

    # Gerando sua própria chave Diffie-Hellman
    parameters = alice_public_key_dh.parameters()
    private_key_dh_bob = parameters.generate_private_key()
    public_key_dh_bob = private_key_dh_bob.public_key()

    # Enviar chave pública Diffie-Hellman para Alice
    serialized_public_dh_bob = public_key_dh_bob.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    s.sendall(serialized_public_dh_bob)

    # Gerando a chave compartilhada
    shared_key_bob = private_key_dh_bob.exchange(alice_public_key_dh)
    derived_key_bob = hashes.Hash(hashes.SHA256(), backend=default_backend())
    derived_key_bob.update(shared_key_bob)
    hmac_key_bob = derived_key_bob.finalize()
    print(f"[Bob] HMAC Key: {hmac_key_bob.hex()}")  # Debug

    # Enviando uma mensagem para Alice com HMAC
    h_bob = hmac.HMAC(hmac_key_bob, hashes.SHA256(), backend=default_backend())
    message_to_send = "Olá, Alice!".encode()
    h_bob.update(message_to_send)
    generated_hmac = h_bob.finalize()

    s.sendall(len(message_to_send).to_bytes(4, "big"))
    s.sendall(message_to_send)
    s.sendall(len(generated_hmac).to_bytes(4, "big"))
    s.sendall(generated_hmac)

