import socket

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 4041
ADDR = (SERVER_IP, PORT)
MSG_LENGTH = 128
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def chat_receive():
    while True:
        msg_length = client.recv(MSG_LENGTH).decode(FORMAT)
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print(msg)


def main():
    chat_receive()


if __name__ == '__main__':
    main()