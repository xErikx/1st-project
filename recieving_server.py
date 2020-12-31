import socket
import threading
import queue
import helper
import datetime
import json

MSG_LENGTH = 128
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
SERVER_EXIT = "!QUIT"
GLOBAL_QUEUE = queue.Queue()
USERS = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def chat_connect(conn, addr):  # chat_connection to our server
    users_checking_config()

    print(f"[CONNECTION] new {addr} connected")

    connection = True

    #####

    # here receive from client the client's name and then store it in a variable, then use it when printing messages

    #####

    client_creds = helper.recv_msg(conn)
    if client_creds["operation"] == "login":
        if client_creds["user_name"] in USERS:
            if client_creds["password"] == USERS[client_creds["user_name"]]["password"]:
                helper.send_msg(conn, {"status": True})
            else:
                helper.send_msg(conn, {"status": False})
                conn.close()
                return
        else:
            helper.send_msg(conn, {"status": False})
            conn.close()
            return
    elif client_creds["operation"] == "register":
        USERS[client_creds["user_name"]] = {"name": client_creds["name"], "password": client_creds["password"]}
        helper.send_msg(conn, {"status": True})
        config_write()

    # {"user_name" : user_name, "password": password}

    client_name = ""
    while connection:

        # Waiting for a message from client 
        msg = helper.recv_msg(conn)["msg"]
        # current message date variable
        now = datetime.datetime.now()

        print("got message")
        if msg != -1:
            # adding the message to the message queue
            GLOBAL_QUEUE.put(f"[{addr}] {client_name}: {msg}: ({now.strftime('%Y-%m-%d %H:%M:%S')})")

        # printing the message 
        print(f"[{addr}] {client_name}: {msg}")

        # returning to the client that the message arrived 
        helper.send_msg(conn, {"msg": "Msg received"})

        # closing the server
    conn.close()


def server_write_to_file():
    """
        Here writing to file
    """

    global GLOBAL_QUEUE

    while True:
        # Getting a received message from queue
        returned_msg = GLOBAL_QUEUE.get()

        # writing to file 
        msg_file_save(returned_msg + "\n")

        # done with the message 
        GLOBAL_QUEUE.task_done()


def msg_file_save(sample_msg):
    f = open("ChatMassages.txt", mode="a")
    f.write(sample_msg)
    f.close()


def users_checking_config():
    global USERS
    f = open("Config.json", mode="r")
    USERS = json.load(f)
    f.close()


def config_write():
    global USERS
    f = open("Config.json", mode="w")
    # storing Users and file into json
    json.dump(USERS, f)
    f.close()


def start_server():
    # starting the server - don't touch 
    server.listen()
    print(f"Server is listening on {SERVER}")

    while True:
        # getting a connection with client
        conn, addr = server.accept()

        # stating the communication with client - every client will work on own function
        thread = threading.Thread(target=chat_connect, args=(conn, addr))
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def main():
    # start_servering a thread which will always get messages from queue and write to file
    # list_thread = threading.Thread(target=server_write_to_file)
    # list_thread.start()

    # start_servering our server
    start_server()


if __name__ == '__main__':
    main()
