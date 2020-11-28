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



def main():
    global USERS
    config = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Config.json", mode="r")
    USERS = json.load(config)

    print("Would you lake to register or you're registered already?")
    print("Press 1 to register, Press 2 if you're registered")
    choice = int(input())
    if choice == 1:
        nickname = input("Enter your nickname: ")
        name = input("Enter your name: ")
        USERS[nickname] = name

    nickname = input("Enter your nickname: ")
    while True:
        message = input()
        send(USERS[nickname], message)
        if message == "exit":
            print("Goodbye")
            break

    f = open("C:\\Users\\ernes\\Documents\\Code\\IntIdea codes\\1st-project\\Config.json", mode="w")
    json.dump(USERS, f)
    f.close()

if __name__ == '__main__':
    main()