import socket

client_socket = None


def connect(host, port):
    global client_socket
    client_socket = socket.socket()
    client_socket.connect((host, port))


def send_text(text):
    client_socket.send(text.encode())


def receive_text(size=1024):
    text = client_socket.recv(size).decode()
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
    client_socket.close()
