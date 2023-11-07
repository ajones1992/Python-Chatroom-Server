import threading
import socket
import sys
import csv
from pathlib import Path

'''
AUTHOR: Alex Jones

Comments that are formatted "[INS #]" correspond to the instruction list. The lines with those comments are implementations of the instruction that is listed.

Upon migrating the files to Linux I discovered some compilation differences that led to bugs. The outcome of fixing those bugs is a somewhat unrefined program.
Some of the lines below may not need to exist, but it works for its intended purpose and will be left as such.
'''

# Make sure the correct amount of arguments is sent. We need an IP.
if len(sys.argv) < 2:
    print('SYNTAX: python CRserver.py {host IP}')
    quit()

# Open the server [INS #1]
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((sys.argv[1], 7890))

# Dictionary used to track active clients
activeClients = {}


# Function to be used to verify username and password with the storage file
def check_user(username, password):
    users = Path('users.csv')
    found = False
    # Read the file
    with users.open('r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', dialect='unix')
        # next(reader)
        # Check the file for existing entry match
        for row in reader:
            if username == row['username']:
                found = True
                if row['password'] == password:
                    return True
                else:
                    return False
        # Create new entry
        if not found:
            save_user(username, password)
            return True


# Helper function to create a new entry in the file
def save_user(username, password):
    output = Path('users.csv')
    output.parent.mkdir(exist_ok=True)
    with output.open('a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='unix')
        writer.writerow({'username': f'{username}', 'password': f'{password}'})


# Function used to broadcast Public Messages
def broadcast(message, sender):
    payload = sender + ': ' + message
    for client in activeClients:
        server.sendto(payload.encode(), client)


# Function used to send Direct Messages
def direct_m(message, sender, receiver):
    payload = 'DIRECT FROM ' + activeClients[sender] + ': ' + message
    rec_c = ''
    for key in activeClients:
        if activeClients[key] == receiver:
            rec_c = key
    if rec_c == '':                                                             # [INS #11.a.v-vi]
        server.send('User is not active. Message not sent.'.encode(), sender)
    else:
        server.sendto(payload.encode(), rec_c)


# Function to receive and communicate with clients [INS #8]
def receive():
    while True:
        try:
            message, address = server.recvfrom(1024)
            message = message.decode()
            match message[0:2]:
                case 'US':
                    # First message should be "USER: xxx ; PASS: xxx" [INS #4, #6, #7]
                    activeClients[address] = message[6:message.index(';') - 1]
                    pass_acc = False
                    password = message[message.index(';') + 8:]
                    pass_acc = check_user(activeClients[address], password)
                    if not pass_acc:
                        server.sendto('NPW'.encode(), address)
                    else:
                        server.sendto('ACK PW'.encode(), address)
                case 'DP':
                    if message[2] == 'N':
                        server.sendto('C PM RE-ACK'.encode(), address)
                        continue
                    # Public message
                    broadcast(message[3:], activeClients[address])                      # [INS #11.1.iv]
                    # Send ACK
                    server.sendto('C PM ACK'.encode(), address)                         # [INS #11.1.v]
                case 'DD':
                    if message[2] == 'N':
                        server.sendto('C DM RE-ACK'.encode(), address)
                        continue
                    # Direct message
                    # Format: "DD [receiver] message"
                    stop_p = message.index(']')
                    direct_m(message[stop_p + 2:], address, message[4:stop_p])
                    # Send ACK
                    server.sendto('C DM ACK'.encode(), address)                         # [INS #11.a.viii]
                case 'DE':                                                              # [INS #11.b.i]
                    # Exit command
                    broadcast(message[3:], activeClients[address])
                    activeClients.pop(address)                                          # [INS #11.b.ii]
                case 'CR':
                    # Handle command
                    print(message)
                case _:
                    # Default send NAK
                    server.sendto(f'NAK handle code needed. Message received: \n {message}'.encode(), address)
        except:
            break


# User side notification that the server is active
print("Server is listening...")
thread = threading.Thread(target=receive)
thread.start()
