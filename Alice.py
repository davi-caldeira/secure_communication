import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.asymmetric import dh

# Funções auxiliares para a troca de chaves Diffie-Hellman
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
private_key_dh = parameters.generate_private_key()
public_key_dh = private_key_dh.public_key()

# Configurações do socket
host = '127.0.0.1'
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print("Alice esperando Bob...")
    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)

        # Enviar chave pública Diffie-Hellman para Bob
        serialized_public = public_key_dh.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        conn.sendall(serialized_public)

        # Receber chave pública Diffie-Hellman de Bob
        bob_serialized_public_dh = conn.recv(1024)
        bob_public_key_dh = serialization.load_pem_public_key(bob_serialized_public_dh, backend=default_backend())

        # Gerando a chave compartilhada
        shared_key = private_key_dh.exchange(bob_public_key_dh)
        derived_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        derived_key.update(shared_key)
        hmac_key = derived_key.finalize()
        print(f"[Alice] HMAC Key: {hmac_key.hex()}")  # Debug

        # Recebendo e verificando a mensagem de Bob
        message_length = int.from_bytes(conn.recv(4), "big")
        message = conn.recv(message_length)
        hmac_length = int.from_bytes(conn.recv(4), "big")
        received_hmac = conn.recv(hmac_length)

        h = hmac.HMAC(hmac_key, hashes.SHA256(), backend=default_backend())
        h.update(message)
        computed_hmac = h.copy().finalize()
        print(f"[Alice] Computed HMAC: {computed_hmac.hex()}")  # Debug

        try:
            h.verify(received_hmac)
            print("Mensagem recebida de Bob:", message.decode())
        except:
            print("A mensagem foi adulterada!")

