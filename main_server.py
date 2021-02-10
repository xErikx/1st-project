import recieving_server
import sending_server
import threading
import requests
from time import sleep


def receiving_thread():
    receiving_server_thread = threading.Thread(target=recieving_server.main)
    receiving_server_thread.start()


def sending_thread():
    sending_server_thread = threading.Thread(target=sending_server.main)
    sending_server_thread.start()
# recieving_server.GLOBAL_QUEUE > sending_server.LIST_MASSAGES


# def queue_to_list_check():
#     while True:
#         queue_new_msg = recieving_server.GLOBAL_QUEUE.get()
#         recieving_server.msg_file_save(queue_new_msg)
#         sending_server.LIST_MASSAGES.append(queue_new_msg)

def telegram_client_msg_receiving():
    last_message_id = 0
    token = "1698512750:AAHYWLH6sdTi6kIVJbTBpqjrBneZgt9rS8w"
    url = f'https://api.telegram.org/bot{token}/getUpdates'

    while True:
        response = requests.post(url)
        for message in response.json()["result"]:
            if last_message_id != 0 and last_message_id >= message['message']['message_id']:
                continue

            sending_server.LIST_MASSAGES.append(message["message"]["text"])

            last_message_id = message['message']['message_id']

        sleep(5)



def queue_thread():
    queue_thread_start = threading.Thread(target=telegram_client_msg_receiving)
    queue_thread_start.start()


def main():
    queue_thread()
    receiving_thread()
    sending_thread()
    input("Press any key to stop the server ")


if __name__ == '__main__':
    main()