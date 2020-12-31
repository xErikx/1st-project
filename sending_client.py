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


def chat_login(chat_socket):
    # Using global variable USERS dictionary
    global USERS
    # registration options for chat program
    print("Would you lake to register or you're registered already?")
    print("Press 1 to register, Press 2 if you're registered")
    choice = int(input())
    if choice == 2:
        user_name = input("Enter your nickname: ")
        password = input("Enter your password: ")
        helper.send_msg(chat_socket, {"operation": "login", "user_name": user_name, "password": password})
        status = helper.recv_msg(chat_socket)["status"]
        print(status)
        if not status:
            return False
    elif choice == 1:
        nickname = input("Enter your nickname: ")
        user_name = input("Enter your name: ")
        password = input("Enter your password: ")
        helper.send_msg(chat_socket, {"operation": "register", "user_name": nickname, "name": user_name, "password": password})
        status = helper.recv_msg(chat_socket)["status"]
        print(status)
        if not status:
            return False
    return user_name


def chat_print():
    global USERS

    # Here we are connecting to our server
    # returns a socket to the server, we need to pass it to the helper functions
    chat_socket = helper.connect_to_server(ADDR)
    nickname = chat_login(chat_socket)

    if not nickname:
        chat_socket.close()
        return
    # sending user name to the server
    while True:

        # Get input from the user
        message = input()

        if message == "exit":
            print("Goodbye")

            # sending exit to the server so the server will close connection 
            helper.send_msg(chat_socket, {"msg": SERVER_EXIT})

            # getting server response - "Msg Received"
            print(helper.recv_msg(chat_socket)["msg"])

            break
        elif message == SERVER_EXIT:

            # server exit command - invalid command for client 
            print("You can't use this command")
            print('If you want to exit the server, enter "exit" command')
            continue

        # writing the message to the file (local, not sending to the server)
        write_to_file(USERS[nickname], message)

        # sending the user input to the server
        helper.send_msg(chat_socket, {"msg": message})

        # getting server response - "Msg Received"
        print(helper.recv_msg(chat_socket)["msg"])


def config_write():
    global USERS
    f = open("Config.json", mode="w")
    # storing Users and file into json
    json.dump(USERS, f)
    f.close()


def main():
    config_load()
    chat_print()
    config_write()


if __name__ == '__main__':
    main()
