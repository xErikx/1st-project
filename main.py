import datetime
import socket
import json

USERS = {}
MSG_LENGTH = 128
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
SERVER_EXIT = "!QUIT"


def send(name, message):
    # making variable for date and time
    now = datetime.datetime.now()
    # opening file in `append` mode
    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Chat.txt", mode="a")
    print(f"{name}: {message}"
          f" {now.strftime('%Y-%m-%d %H:%M:%S')}")
    # writing name, massage and date/time into file
    f.write(f"{name}: {message} {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    # closing the file after it's use (mandatory)
    f.close()


def config_load():
    global USERS
    # opening json configuration file for names and nicknames
    config = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Config.json", mode="r")
    USERS = json.load(config)


def chat_login():
    # Using global variable USERS dictionary
    global USERS
    # registration options for chat program
    print("Would you lake to register or you're registered already?")
    print("Press 1 to register, Press 2 if you're registered")
    choice = int(input())
    if choice == 1:
        nickname = input("Enter your nickname: ")
        name = input("Enter your name: ")
        USERS[nickname] = name
    else:
        nickname = input("Enter your nickname: ")
    return nickname


def chat_print(nickname):
    global USERS
    # connecting client to the server for the messages
    chat = connect_to_server()
    while True:
        message = input()
        if message == "exit":
            print("Goodbye")
            send_msg(SERVER_EXIT, chat)
            break
        elif message == SERVER_EXIT:
            print("You can't use this command")
            print('If you want to exit the server, enter "exit" command')
            continue
        send(USERS[nickname], message)
        send_msg(message, chat)


def connect_to_server():
    # Chat connection to the server
    chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client connection to IP address and Port
    chat.connect(ADDR)
    # returning variable `chat` for the chat_print function connection
    return chat


def send_msg(msg, socket):
    # initial message which must be sent
    message = msg.encode(FORMAT)
    # variable for message char length as integer
    msg_length = len(message)
    # converting length into str and formatting into `utf-8`
    send_length = str(msg_length).encode(FORMAT)
    # refilling the empty bytes with a space so that we can send the full length
    send_length += b' ' * (MSG_LENGTH - len(send_length))
    # sending to the socket the full length including the message
    socket.send(send_length)
    # sending the main message to the client
    socket.send(message)
    # printing out the receive in 2048 bytes
    print(socket.recv(2048).decode(FORMAT))


def config_write():
    global USERS
    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Config.json", mode="w")
    # storing Users and file into json
    json.dump(USERS, f)
    f.close()


def main():
    config_load()
    nickname = chat_login()
    chat_print(nickname)
    config_write()


if __name__ == '__main__':
    main()
