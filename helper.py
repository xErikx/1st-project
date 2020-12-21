import socket

MSG_LENGTH = 128
FORMAT = "utf-8"
SERVER_EXIT = "!QUIT"

def send_msg(socket, msg):
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


def recv_msg(socket):
    msg_length = socket.recv(MSG_LENGTH).decode(FORMAT)  # formatting msg's from chat in length
    
    msg = -1

    if msg_length:  # if msg's are not empty
        
        msg_length = int(msg_length)  # reformat length from str to int
        msg = socket.recv(msg_length).decode(FORMAT)  # receiving messages and formatting them
        
        if msg == SERVER_EXIT:  # Server exit
            return -1 

    return msg

def connect_to_server(address):
    """
        Creating a socket with the server, no need to touch this function
    """
    
    # Chat connection to the server
    chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # client connection to IP address and Port
    chat.connect(address)
    # returning variable `chat` for the chat_print function connection
    
    return chat