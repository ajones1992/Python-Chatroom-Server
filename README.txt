INCLUDED FILES:
	TCP_chatserver.py
	TCP_chatclient.py
	UDP_chatserver.py
	UDP_chatclient.py
	csv_setup.py
	users.csv


Running the TCP chatroom:

1) Open a new terminal window
2) Navigate directories to where the TCP_chatserver.py file is stored
3) Type: "python TCP_chatserver.py {IP} {PORT}" into the command line
	a) {IP} is the IP address the server will run on
	b) {PORT} is the port number the server will socket to
4) The command line should display "The server is listening..."
5) Open a new terminal window
6) Navigate directories to where the TCP_chatclient.py file is stored
7) Type: "python TCP_chatclient.py {IP} {PORT}" into the command line
	a) {IP} is the IP address the client will run on
	b) {PORT} is the port number the client will socket to
8) The program will display prompts and expect inputs for chat processes


Running the UDP chatroom:

1) Open a new terminal window
2) Navigate directories to where the UDP_chatserver.py file is stored
3) Type: "python UDP_chatserver.py {IP}" into the command line
	a) {IP} is the IP address the server will run on
4) The command line should display "The server is listening..."
5) Open a new terminal window
6) Navigate directories to where the UDP_chatclient.py file is stored
7) Type: "python UDP_chatclient.py {IP} {PORT}" into the command line
	a) {IP} is the IP address the client will run on
	b) {PORT} is the port number the client will socket to
8) The program will display prompts and expect inputs for chat processes


The users.csv file is where usernames and passwords are stored. It must be in the same directory as the TCP/UDP server file. 
If one does not already exist, execute the csv_setup.py file. This will create the users.csv file correctly.
