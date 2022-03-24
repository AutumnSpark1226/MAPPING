import socket

server_socket = None


def server_start(port):
    global server_socket
    host = socket.gethostname()
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen()


def accept_client():
    connection, client_address = server_socket.accept()
    return connection, client_address


def send_text(connection, text):
    connection.send(text.encode())


def receive_text(connection, size=1024):
    data = connection.recv(size).decode()
    text = str(data)
    return text


if __name__ == '__main__':
    # simple echo server to test the communication
    server_start(6666)
    conn, address = accept_client()
    while True:
        test_message = receive_text(conn)
        if not test_message:
            break
        print("received: " + test_message)
        send_text(conn, test_message)
    conn.close()
