import socket
import helper 

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 4041
ADDR = (SERVER_IP, PORT)
MSG_LENGTH = 128
FORMAT = "utf-8"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)


def chat_receive():
    # receiving messages from server
    while True:
        
        # waiting for a message from server
        msg = helper.recv_msg(client_socket)["msg"]
        print(msg)


def main():

    chat_receive()


if __name__ == '__main__':
    main()