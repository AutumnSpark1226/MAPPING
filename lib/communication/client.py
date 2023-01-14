import socket

_client_socket = None

"""
the communication client
not further explanation needed
"""


def connect(host, port):
    global _client_socket
    _client_socket = socket.socket()
    _client_socket.connect((host, port))


def disconnect():
    if not _client_socket:
        raise Exception("client not connected")
    _client_socket.close()


def send_text(text: str):
    if not _client_socket:
        raise Exception("client not connected")
    buffer = text.encode() + b'\x04'
    _client_socket.send(buffer)


def receive_text():
    if not _client_socket:
        raise Exception("client not connected")
    buffer = b''
    received_byte = b''
    while received_byte != b'\x04':
        buffer += received_byte
        received_byte = _client_socket.recv(1)
    return buffer.decode()


if __name__ == '__main__':
    import os

    # simple echo client to test the communication
    server_ip = open(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + '/host.txt',
                     'r').readline().rstrip()
    connect(server_ip, 6666)
    while True:
        test_message = input("> ")
        send_text(test_message)
        if test_message == 'disconnect':
            break
        test_message = receive_text()
        print('received: ' + test_message)
    disconnect()
