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
    now = datetime.datetime.now()
    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Chat.txt", mode="a")
    print(f"{name}: {message}"
          f" {now.strftime('%Y-%m-%d %H:%M:%S')}")
    f.write(f"{name}: {message} {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.close()


def config_load():
    global USERS
    config = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Config.json", mode="r")
    USERS = json.load(config)


def chat_login():
    global USERS
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
    chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat.connect(ADDR)
    return chat


def send_msg(msg, socket):
    message = msg.encode(FORMAT) # 'welcome'
    msg_length = len(message) # 7
    send_length = str(msg_length).encode(FORMAT) #  7
    send_length += b' ' * (MSG_LENGTH - len(send_length)) #
    socket.send(send_length)
    socket.send(message)
    print(socket.recv(2048).decode(FORMAT))


def config_write():
    global USERS
    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Config.json", mode="w")
    json.dump(USERS, f)
    f.close()


def main():
    config_load()
    nickname = chat_login()
    chat_print(nickname)
    config_write()


if __name__ == '__main__':
    main()
