import socket
import threading
import sys
import time

'''
AUTHOR: Alex Jones

Comments that are formatted "[INS #]" correspond to the instruction list. The lines with those comments are implementations of the instruction that is listed.

Upon migrating the files to Linux I discovered some compilation differences that led to bugs. The outcome of fixing those bugs is a somewhat unrefined program.
Some of the lines below may not need to exist, but it works for its intended purpose and will be left as such.
'''

# Make sure the correct amount of arguments is sent. We need an IP and Port Number.
if len(sys.argv) < 3:
    print('SYNTAX: python CRclient.py {host IP} {port num}')
    quit()

m_status = False

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((sys.argv[1], int(sys.argv[2])))

# Identify the client for the server  [INS #3, #5]
username = input("Enter username: ")
client.send(username.encode())
message = None
while message != 'C ACK USER':
    message = client.recv(1024).decode()
password = input("Enter password: ")
client.send(password.encode())
# If password doesn't match, send a new one
message = None
while message is None:
    message = client.recv(1024).decode()
if message == 'NPW':
    pass_acc = False
    while not pass_acc:
        password = input('Wrong password try again: ')
        client.send(password.encode())
        message = client.recv(1024).decode()
        if message == 'ACK PW':
            pass_acc = True


# Communicating with Server  [INS #9, #10]
def handle():
    global m_status
    counter = 0
    while True:
        try:
            operation = input("Choose an operation (P/D/E): ")
            match operation:
                case "P":                                                       # [INS #11.1]
                    # Public message
                    public_payload = input('What is your message? ')
                    client.send(f'DP {public_payload}'.encode())                # [INS #11.1.i-iii]
                    while not m_status:                                         # [INS #11.1.v-vi]
                        time.sleep(1)
                        if counter == 5:
                            client.send(f'DPN'.encode())
                            counter = 0
                            continue
                        counter += 1
                    m_status = False
                case "D":                                                       # [INS #11.a]
                    # Direct message
                    direct_payload = input('What is your message? ')
                    rec = input('Who are you sending it to? ')
                    client.send(f'DD [{rec}] {direct_payload}'.encode())        # [INS #11.a.0/iv]
                    while not m_status:                                         # [INS #11.a.ix-x]
                        time.sleep(1)
                        if counter == 5:
                            client.send(f'DDN'.encode())
                            counter = 0
                            continue
                        counter += 1
                        continue
                    m_status = False
                case "E":                                                       # [INS #11.b]
                    # Exit command
                    client.send(f'DE {username} is logging off. TTYL!'.encode())  # [INS #11.b.0]
                    receive_thread.join()
                    sys.exit(0)                                            # [INS #11.b.iii]
                case _:
                    print("Please type P, D, or E.")
        except:
            # Close connection when error occurs
            print("An error occured!")
            client.send(f'DE {username} has disconnected.'.encode())
            client.close()
            break


# Function to print messages sent to the client
def receive():
    while True:
        receive = client.recv(1024).decode()
        message_receiver(receive)
            

def message_receiver(receive):
    global m_status
    if len(receive) > 0:
        if receive[0:2] == 'C ':
            if receive[2] == 'P':
                m_status = True
            elif receive[2] == 'D':
                m_status = True
            else:
                pass
        else:
            print(receive)                                                          # [INS #11 ALL DISPLAY INSTRUCTIONS]



# Thread initialization
handle_thread = threading.Thread(target=handle)
handle_thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()
