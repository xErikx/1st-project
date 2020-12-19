import socket
import threading


SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 4041
MSG_LENGTH = 128
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"
LIST_MASSAGES = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send_message_to_client(msg, connection):
    msg = msg.encode(FORMAT)
    # We need for that 7 boxes - 1 box per char
    msg_length = len(msg)

    # We need to convert the number of boxes from INT to String
    # so we will know how many boxes we need to send the LEN on message
    # Every char is a Box !
    msg_length = str(msg_length)

    # getting number of  boxes we need for sending the length of the original message
    send_length_boxes_count = len(msg_length)

    # buffer = <the length of the of the original message>
    # + <empty boxes> * <number of total boxes - number of the boxes we use for sending the length>
    buffer = msg_length.encode(FORMAT) + b' ' * (MSG_LENGTH - send_length_boxes_count)

    # sending the length to the client
    connection.send(buffer)

    # sending the message to the client
    connection.send(msg)


def client_handling(connection, address):
    # we want to send 'Welcome'
    msg = "Welcome"

    print(f"[CONNECTED] to {address}")

    # Here we're calling this function which sends the message to the client
    # Sending 'Welcome' to the client!
    send_message_to_client(msg, connection)

    # list counter (so we will know where we are inside the list!)
    index = 0
    while True:

        # check if the index is inside the list , or we got to the end
        if index == len(LIST_MASSAGES):
            continue
        else:
            # if inside the list - sending the message to the client
            send_message_to_client(LIST_MASSAGES[index], connection)

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
    server.listen()
    print(f"Server is listening on {SERVER_IP}")
    while True:
        connection, address = server.accept()
        client_thread = threading.Thread(target=client_handling, args=(connection, address))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def main():
    # making thread for reading_lines function
    list_thread = threading.Thread(target=reading_lines_in_file)
    list_thread.start()
    server_start()


if __name__ == '__main__':
    main()