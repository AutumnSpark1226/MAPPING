import socket

_client_socket = None
_aes_key = None
_iv = None


def connect(host, port):
    global _client_socket
    _client_socket = socket.socket()
    _client_socket.connect((host, port))


def disconnect():
    if not _client_socket:
        raise Exception("client not connected")
    _client_socket.close()


def send_text(text):
    if not _client_socket:
        raise Exception("client not connected")
    _client_socket.send(text.encode())


def receive_text(size=1024):
    if not _client_socket:
        raise Exception("client not connected")
    return _client_socket.recv(size).decode()


if __name__ == '__main__':
    # simple echo client to test the communication
    host = "192.168.0.2"
    connect(host, 6666)
    while True:
        test_message = input("> ")
        send_text(test_message)
        if test_message == 'disconnect':
            break
        test_message = receive_text()
        print('received: ' + test_message)
    disconnect()
