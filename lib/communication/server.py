import socket

_server_socket: socket.socket


def start(port: int):
    global _server_socket
    _server_socket = socket.socket()
    _server_socket.bind(('0.0.0.0', port))
    _server_socket.listen()


def stop():
    if not _server_socket:
        raise Exception("server not running")
    _server_socket.close()


def accept_client():
    if not _server_socket:
        raise Exception("server not running")
    connection, client_address = _server_socket.accept()
    return connection, client_address


def send_text(connection: socket.socket, text: str):
    if not _server_socket:
        raise Exception("server not running")
    connection.send(text.encode())


def receive_text(connection: socket.socket, size=1024):
    if not _server_socket:
        raise Exception("server not running")
    text = connection.recv(size).decode()
    return text


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
