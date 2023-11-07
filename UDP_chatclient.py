import socket
import threading
import sys

'''
AUTHOR: Alex Jones

Comments that are formatted "[INS #]" correspond to the instruction list. The lines with those comments are implementations of the instruction that is listed.

Upon migrating the files to Linux I discovered some compilation differences that led to bugs. The outcome of fixing those bugs is a somewhat unrefined program.
Some of the lines below may not need to exist, but it works for its intended purpose and will be left as such.
'''

# Make sure the correct amount of arguments is sent. We need an IP and Port Number.
if len(sys.argv) < 3 or sys.argv[2] == '7890':
    print('SYNTAX: python CRclient.py {host IP} {port num}\nDO NOT USE 7890.')
    quit()

m_status = False

# Connecting To Server [INS #2]
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((sys.argv[1], int(sys.argv[2])))

# Identify the client for the server [INS #3, #5]
username = input("Enter username: ")
password = input("Enter password: ")
client.sendto(f'USER: {username} ; PASS: {password}'.encode(), (sys.argv[1], 7890))
# If password doesn't match, send a new one
message, addr = client.recvfrom(1024)
message = message.decode()
if message == 'NPW':
    pass_acc = False
    while not pass_acc:
        password = input('Wrong password try again: ')
        client.sendto(f'USER: {username} ; PASS: {password}'.encode(), (sys.argv[1], 7890))
        message, addr = client.recvfrom(1024)
        message = message.decode()
        if message == 'ACK PW':
            pass_acc = True


# Communicating with Server [INS #9, #10]
def handle():
    global m_status
    counter = 0
    while True:
        try:
            operation = input("Choose an operation (P/D/E): ")
            match operation:
                case "P":                                                                   # [INS #11.1]
                    # Public message
                    public_payload = input('What is your message? ')
                    client.sendto(f'DP {public_payload}'.encode(), (sys.argv[1], 7890))     # [INS #11.1.i-iii]
                    while not m_status:                                                     # [INS #11.1.v-vi]
                        if counter == 5:
                            client.sendto('DPN'.encode(), (sys.argv[1], 7890))
                            counter = 0
                            continue
                        counter += 1
                        continue
                    m_status = False
                case "D":                                                                   # [INS #11.a]
                    # Direct message
                    direct_payload = input('What is your message? ')
                    rec = input('Who are you sending it to? ')
                    client.sendto(f'DD [{rec}] {direct_payload}'.encode(), (sys.argv[1], 7890))  # [INS #11.a.0/iv]
                    while not m_status:                                                     # [INS #11.a.ix-x]
                        if counter == 5:
                            client.sendto('DDN'.encode(), (sys.argv[1], 7890))
                            counter = 0
                            continue
                        counter += 1
                        continue
                    m_status = False
                case "E":                                                                   # [INS #11.b]
                    # Exit command
                    client.sendto(f'DE {username} is logging off. TTYL!'.encode(), (sys.argv[1], 7890))  # [INS #11.b.0]
                    receive_thread.join()
                    quit()                                                                  # [INS #11.b.iii]
                case _:
                    print("Please type P, D, or E.")
        except:
            # Close connection when error occurs
            print("An error occured!")
            client.sendto(f'DE {username} has disconnected.'.encode(), (sys.argv[1], 7890))
            quit()


# Function to print messages sent to the client
def receive():
    global m_status
    while True:
        delivery, _ = client.recvfrom(1024)
        delivery = delivery.decode()
        if delivery[0:2] == 'C ':
            if delivery[2] == 'P':
                m_status = True
                continue
            elif delivery[2] == 'D':
                m_status = True
                continue
        print(delivery)                         # [INS #11 ALL DISPLAY INSTRUCTIONS]


# Thread initialization
receive_thread = threading.Thread(target=receive)
receive_thread.start()

handle_thread = threading.Thread(target=handle)
handle_thread.start()
