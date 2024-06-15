# Secure File Transfer Server using AES Encryption

This project implements a secure file transfer server using AES encryption in GCM mode. It allows clients to securely send files to the server, which are then decrypted and saved. Additionally, clients can send messages to the server for real-time communication.

## Features

- Secure AES encryption (GCM mode) for file transfer
- Real-time progress bar for file transfer
- Multi-client support with concurrent connections
- Basic text messaging between clients and server

## How to use
1. Run sever.py first
2. On a different terminal or machine run client.py
3. To send a file you have to use '#Send_File'
4. Communicate!

## Requirements

- Python 3.x
- cryptography library (`pip install cryptography` and `pip install pycryptodome`)
- tqdm library (`pip install tqdm`)

## How can it be improved

- Ensuring two way communication between sever and clients
- Using the information sent to sever in other server making it a large network
  


