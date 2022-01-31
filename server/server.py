from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []


def broad_cast(msg, name):
    """
    read new message to all clients
    :param msg: bytes['utf-8]
    :param name: str
    :return: None
    """
    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf-8") + msg)


def client_connection(person):
    """
    Thread to handle messages from all client
    :param client: Person
    :return: None
    """
    client = person.client
    name = person.name
    addr = person.addr

    # GET PERSON'S NAME
    name = client.recv(BUFSIZ).decode('utf-8')
    msg = f"{name} has joined the chat!"
    broad_cast(msg)

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf-8"):
            broad_cast(f"{name} has left the chat...")
            client.close()
            persons.remove(person)
        else:
            client.send(msg, name)


def wait_for_connection(SERVER):
    """
    Wait for connection from new clients, start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            person.append(person)
            print(f"[CONNECTION] {addr} connected to the server✅")
            Thread(target=client_connection, args=(client,)).start()
        except Exception as e:
            print('FAILURE', e)
            run = False


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS)  # listen for connection
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
