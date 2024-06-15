import socket
import tqdm
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Constants
key = b"thisisasecretkey"
nonce = b"thisauniquenonce"
backend = default_backend()
encoder = "utf-8"
host = socket.gethostbyname(socket.gethostname())
port = 12345
byte_size = 4096
separator = "<separator>"

def send_file(client_socket):
    file_path = input("Enter file path: ")
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=backend)
    encryptor = cipher.encryptor()

    with open(file_path, "rb") as f:
        file_data = f.read()

    encrypted_data = encryptor.update(file_data) + encryptor.finalize()
    tag = encryptor.tag

    client_socket.send(f"{file_name}{separator}{len(encrypted_data) + len(tag)}".encode(encoder))

    progress = tqdm.tqdm(range(len(encrypted_data) + len(tag)), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

    client_socket.sendall(encrypted_data + tag)
    progress.update(len(encrypted_data + tag))

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Client connected to server at {host}:{port}")

    while True:
        msg = input("Client: ")
        client_socket.send(msg.encode(encoder))

        if msg == "quit":
            break
        elif "#Send_File" in msg:
            send_file(client_socket)
        else:
            try:
                server_msg = client_socket.recv(byte_size).decode(encoder)
                print(f"Server: {server_msg}")
            except Exception as e:
                print(f"Error: {e}")
                break

    client_socket.close()

if __name__ == "__main__":
    main()
