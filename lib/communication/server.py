import socket

_server_socket: socket.socket

"""
the communication client
not further explanation needed
"""


def start(port: int):
    global _server_socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    _server_socket = socket.socket()
    _server_socket.bind(("0.0.0.0", port))  # FIXME
    _server_socket.listen()


def stop():
    if not _server_socket:
        raise Exception("server not running")
    _server_socket.close()


def accept_client():  # clients won't be automatically accepted; calling this function will accept one client
    if not _server_socket:
        raise Exception("server not running")
    connection, client_address = _server_socket.accept()
    return connection, client_address


def send_text(connection: socket.socket, text: str):
    if not _server_socket:
        raise Exception("server not running")
    buffer = text.encode() + b'\x04'
    connection.send(buffer)


def receive_text(connection: socket.socket):
    if not _server_socket:
        raise Exception("server not running")
    buffer = b''
    received_byte = b''
    while received_byte != b'\x04':
        buffer += received_byte
        received_byte = connection.recv(1)
    return buffer.decode()


if __name__ == '__main__':
    # simple echo server to test the communication
    start(6666)
    conn, address = accept_client()
    while True:
        test_message = receive_text(conn)
        if test_message == 'disconnect':
            break
        print("received: " + test_message)
        send_text(conn, test_message)
    conn.close()
    stop()
