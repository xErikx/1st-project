import datetime
import socket
import json
import helper

USERS = {}
MSG_LENGTH = 128
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
SERVER_EXIT = "!QUIT"


def write_to_file(name, message):
    # making variable for date and time
    now = datetime.datetime.now()
    # opening file in `append` mode
    f = open("Chat.txt", mode="a")
    print(f"{name}: {message}"
          f" {now.strftime('%Y-%m-%d %H:%M:%S')}")
    # writing name, massage and date/time into file
    f.write(f"{name}: {message} {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    # closing the file after it's use (mandatory)
    f.close()


def config_load():
    global USERS
    # opening json configuration file for names and nicknames
    config = open("Config.json", mode="r")
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
    
    # Here we are connecting to our server
    # returns a socket to the server, we need to pass it to the helper functions
    chat_socket = helper.connect_to_server(ADDR)

    while True:

        # Get input from the user
        message = input()


        if message == "exit":
            print("Goodbye")

            # sending exit to the server so the server will close connection 
            helper.send_msg(chat_socket, SERVER_EXIT)

            # getting server response - "Msg Recieved"
            print(helper.recv_msg(chat_socket))

            break
        elif message == SERVER_EXIT:

            # server exit command - invalid command for client 
            print("You can't use this command")
            print('If you want to exit the server, enter "exit" command')
            continue

        # writing the message to the file (local, not sending to the server)
        write_to_file(USERS[nickname], message)

        # sending the user input to the server
        helper.send_msg(chat_socket, message)

        # getting server response - "Msg Recieved"
        print(helper.recv_msg(chat_socket))



def config_write():
    global USERS
    f = open("Config.json", mode="w")
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
