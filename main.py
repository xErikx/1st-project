import datetime

import json

USERS = {}


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
    while True:
        message = input()
        send(USERS[nickname], message)
        if message == "exit":
            print("Goodbye")
            break


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
