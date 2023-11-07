import socket
import threading
import sys

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
password = input("Enter password: ")
client.send(username.encode())
client.send(password.encode())
# If password doesn't match, send a new one
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
                        if counter == 5:
                            client.send(f'DPN'.encode())
                            counter = 0
                            continue
                        counter += 1
                        continue
                    m_status = False
                case "D":                                                       # [INS #11.a]
                    # Direct message
                    direct_payload = input('What is your message? ')
                    rec = input('Who are you sending it to? ')
                    client.send(f'DD [{rec}] {direct_payload}'.encode())        # [INS #11.a.0/iv]
                    while not m_status:                                         # [INS #11.a.ix-x]
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
                    quit()                                            # [INS #11.b.iii]
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
    global m_status
    while True:
        receive = client.recv(1024).decode()
        if len(receive) > 0:
            if receive[0] == 'C':
                if receive[2] == 'P':
                    m_status = True
                    continue
                elif receive[2] == 'D':
                    m_status = True
                    continue
            print(receive)                                                          # [INS #11 ALL DISPLAY INSTRUCTIONS]


# Thread initialization
receive_thread = threading.Thread(target=receive)
receive_thread.start()

handle_thread = threading.Thread(target=handle)
handle_thread.start()