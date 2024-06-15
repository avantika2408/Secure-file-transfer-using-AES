import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Initialize key and nonce (ensure they are the same as used in the client)
key = b"thisisasecretkey"
nonce = b"thisauniquenonce"
backend = default_backend()
encoder = "utf-8"

# Network configuration
host = socket.gethostbyname(socket.gethostname())
port = 12345
byte_size = 4096
separator = "<separator>"

# Global variable to track active connections
active_connections = 0
active_connections_lock = threading.Lock()

def main():
    global active_connections
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Increment active connections counter
        with active_connections_lock:
            active_connections += 1
            print(f"Active connections: {active_connections}")

        # Handle each client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

def handle_client(client_socket, addr):
    global active_connections
    connected = True
    while connected:
        msg = client_socket.recv(1024).decode(encoder)

        if msg == "quit":
            print(f"Client {addr} disconnected")
            break

        elif "#Send_File" in msg:
            # Receive file info
            received = client_socket.recv(byte_size).decode()
            file_name, file_size = received.split(separator)
            file_name = "received_" + file_name
            file_size = int(file_size)

           

            # Receive and write the encrypted file bytes
            with open(file_name, "wb") as f:
                received_size = 0
                while received_size < file_size:
                    bytes_read = client_socket.recv(byte_size)
                    f.write(bytes_read)
                    received_size += len(bytes_read)
                    

            # Decrypt the received file
            decrypt_file(file_name)

            print(f"File received and decrypted: {file_name}")

            # Send acknowledgment or additional messages if needed
            client_socket.send("File received and decrypted successfully".encode(encoder))

        else:
            print(f"Received message from {addr}: {msg}")

            # Send acknowledgment or response to the client
            response = f"Server received message: {msg}"
            client_socket.send(response.encode(encoder))

    # Decrement active connections counter when client disconnects
    with active_connections_lock:
        active_connections -= 1
        print(f"Active connections: {active_connections}")

    client_socket.close()

def decrypt_file(file_name):
    # Read the encrypted file and decrypt it
    with open(file_name, "rb") as f:
        encrypted_data = f.read()
        tag = encrypted_data[-16:]  # Last 16 bytes of the file is the authentication tag
        encrypted_data = encrypted_data[:-16]  # Remove the last 16 bytes

    # Decrypt the file using AES GCM mode
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Write the decrypted data to a new file
    decrypted_file_name = "decrypted_" + file_name
    with open(decrypted_file_name, "wb") as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    main()

