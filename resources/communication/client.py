import hashlib
import os
import socket

from Crypto.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Util import Padding

client_socket = None
_aes_key = None
_iv = None


def connect(host, port):
    global client_socket
    client_socket = socket.socket()
    client_socket.connect((host, port))
    # receive public_key
    public_key = client_socket.recv(1024)
    # generate _aes_key
    global _aes_key, _iv
    _aes_key = os.urandom(32)
    # generate _iv
    _iv = os.urandom(16)
    # create cipher
    cipher = AES.new(_aes_key, AES.MODE_CBC, _iv)
    # encrypt aes_key
    rsa_public_key = RSA.importKey(public_key)
    oaep_cipher = PKCS1_OAEP.new(rsa_public_key)
    encrypted_aes_key = oaep_cipher.encrypt(_aes_key)
    # send encrypted_aes_key
    client_socket.send(encrypted_aes_key)
    # encrypt iv
    encrypted_iv = oaep_cipher.encrypt(_iv)
    # send encrypted_iv
    client_socket.send(encrypted_iv)
    # receive encrypted_hashed_public_key
    encrypted_hashed_public_key = client_socket.recv(1024)
    # decrypt hashed_public_key
    hashed_public_key = cipher.decrypt(encrypted_hashed_public_key).decode()
    # hash public key
    hashed_public_key2 = hashlib.sha512(public_key).hexdigest()
    # encrypt hashed_public_key2
    encrypted_hashed_public_key2 = cipher.encrypt(hashed_public_key2)
    # send encrypted_hashed_public_key2
    client_socket.send(encrypted_hashed_public_key2)
    # check if hashed_public_key and hashed_public_key2 are equal (they should be)
    if hashed_public_key2 != hashed_public_key:
        client_socket.close()
        raise Exception("encryption or server error")


def disconnect():
    client_socket.close()


def send_text(text):
    padded_text = Padding.pad(text.encode(), 16)
    cipher = AES.new(_aes_key, AES.MODE_CBC, _iv)
    encrypted_text = cipher.encrypt(padded_text)
    client_socket.send(encrypted_text)


def receive_text(size=1024):
    cipher = AES.new(_aes_key, AES.MODE_CBC, _iv)
    encrypted_text = client_socket.recv(size)
    text = str(Padding.unpad(cipher.decrypt(encrypted_text), 16).decode())
    return text


if __name__ == '__main__':
    # simple echo client to test the communication
    connect('bestPCEver', 6666)
    while True:
        test_message = input("> ")
        if test_message == 'disconnect':
            break
        send_text(test_message)
        test_message = receive_text()
        print('received: ' + test_message)
    disconnect()
