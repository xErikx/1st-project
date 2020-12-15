import socket
import threading

MSG_LENGTH = 128
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
SERVER_EXIT = "!QUIT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def chat_connect(conn, addr):  # chat_connection to our server
    print(f"[CONNECTION] new {addr} connected")

    connection = True
    while connection:
        msg_length = conn.recv(MSG_LENGTH).decode(FORMAT)  # formatting msg's from chat in length
        if msg_length:  # if msg's are not empty
            msg_length = int(msg_length)  # reformat length from str to int
            msg = conn.recv(msg_length).decode(FORMAT)  # receiving messages and formatting them
            msg_file_save(msg)
            if msg == SERVER_EXIT:  # Server exit
                connection = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()  # closing the server


def msg_file_save(sample_msg):
    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\ChatMassages.txt", mode="a")
    f.write(sample_msg)
    f.close()


def start():  # server start
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=chat_connect, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def main():
    start()


if __name__ == '__main__':
    main()
