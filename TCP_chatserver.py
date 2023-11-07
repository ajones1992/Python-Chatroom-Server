import threading
import socket
import sys
import csv

# Make sure the correct amount of arguments is sent. We need an IP and Port Number.
if len(sys.argv) < 3:
    print('SYNTAX: python CRserver.py {host IP} {port num}')
    quit()

# Open the server  [INS #1]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((sys.argv[1], int(sys.argv[2])))
server.listen()


# Dictionary used to track active clients
activeClients = {}


# Function to be used to verify username and password with the storage file
def check_user(username, password):
    found = False
    # Read the file
    with open("./users.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        # Check the file for existing entry match
        for row in reader:
            if username == row[0]:
                found = True
                if row[1] == password:
                    return True
                else:
                    return False
        # Create new entry
        if not found:
            save_user(username, password)
            return True


# Helper function to create a new entry in the file
def save_user(username, password):
    with open("./users.csv", 'a', newline='') as csvfile:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'username': f'{username}', 'password': f'{password}'})


# Function used to broadcast Public Messages
def broadcast(message, sender):
    payload = sender + ': ' + message
    for client in activeClients:
        client.send(payload.encode())


# Function used to send Direct Messages
def direct_m(message, sender, receiver):
    payload = 'DIRECT FROM ' + activeClients[sender] + ': ' + message
    rec_c = ''
    for key in activeClients:
        if activeClients[key] == receiver:
            rec_c = key
    if rec_c == '':                                                         # [INS #11.a.v-vi]
        sender.send('User is not active. Message not sent.'.encode())
    else:
        rec_c.send(payload.encode())


# Function used by thread to handle clients
def handle(client):
    # Add client to dictionary
    clientUser = activeClients[client]
    # Communicate with the client
    while True:
        try:
            message = client.recv(1024).decode()
            # Match the message code
            match message[0:2]:
                case 'DP':
                    if message[2] == 'N':
                        client.send('C PM RE-ACK'.encode())
                        continue
                    # Public message
                    broadcast(message[3:], activeClients[client])                       # [INS #11.1.iv]
                    # Send ACK
                    client.send('C PM ACK'.encode())                                    # [INS #11.1.v]
                case 'DD':
                    if message[2] == 'N':
                        client.send('C DM RE-ACK'.encode())
                        continue
                    # Direct message
                    stop_p = message.index(']')
                    direct_m(message[stop_p+2:], client, message[4:stop_p])
                    # Send ACK
                    client.send('C DM ACK'.encode())                                    # [INS #11.a.viii]
                case 'DE':                                                              # [INS #11.b.i]
                    # Exit command
                    broadcast(message[3:], activeClients[client])
                    activeClients.pop(client)                                           # [INS #11.b.ii]
                    client.close()
                case 'CR':
                    # Handle command
                    print(message)
                case _:
                    # Default send NAK
                    client.send(f'NAK handle code needed. Message received: \n {message}'.encode())

        except:
            # If client disconnects
            broadcast('left the chat!', clientUser)
            break


# Function to receive clients and set up the handle thread  [INS #4, #6, #7, #8]
def receive():
    while True:
        client, address = server.accept()
        activeClients[client] = client.recv(1024).decode()
        pass_acc = False
        while not pass_acc:
            password = client.recv(1024).decode()
            pass_acc = check_user(activeClients[client], password)
            if not pass_acc:
                client.send('NPW'.encode())
        client.send('ACK PW'.encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# User side notification that the server is active
print("Server is listening...")
receive()
