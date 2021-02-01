import socket
import helper
import threading
import telegram_send

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 4041
MSG_LENGTH = 128
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"
LIST_MASSAGES = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def client_handling(client_socket, address):
    # we want to send 'Welcome'
    welcome_message = "Welcome"

    print(f"[CONNECTED] to {address}")

    # Here we're calling this function which sends the message to the client
    # Sending 'Welcome' to the client!
    helper.send_msg(client_socket, {"msg": welcome_message})

    # list counter (so we will know where we are inside the list!)
    index = 0
    while True:

        # check if the index is inside the list , or we got to the end
        if index == len(LIST_MASSAGES):
            continue
        else:
            # if inside the list - sending the message to the client
            helper.send_msg(client_socket, {"msg": LIST_MASSAGES[index]})

            # going to the next line - the next Index
            index += 1


def reading_lines_in_file():
    global LIST_MASSAGES

    # reading our database
    f = open("ChatMassages.txt", "r")

    while True:

        # reading file line by line
        new_line = f.readline()

        # if the line is not empty (if line is empty - we got to the EOF)
        if new_line != '':
            # adding the line to the message list
            LIST_MASSAGES.append(new_line)


def server_start():
    # Starting the sending server 
    server.listen()
    print(f"Server is listening on {SERVER_IP}")

    while True:
        # getting connection from client
        connection, address = server.accept()
        client_thread = threading.Thread(target=client_handling, args=(connection, address))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def main():
    # making thread for reading_lines function
    # list_thread = threading.Thread(target=reading_lines_in_file)
    # list_thread.start()
    server_start()


if __name__ == '__main__':
    main()
