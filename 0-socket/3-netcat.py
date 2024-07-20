import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# Takes a command string as input.
def execute(cmd):
    # Strips leading/trailing whitespace.
    cmd = cmd.strip()
    if not cmd:
        return
    # Executes the command using subpocess.check_output(), capturing both stdout and stderr.
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    # Returns the decoded output as a string.   
    return output.decode()

# A class encapsulating the functionality of the NetCat tool.
class NetCat:
    # Initializes with command-line arguments and optionally a buffer for sending data.
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        # Creates a socket object with specific options for reuse address/port. 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Offers methods to either listen for incoming connections (run() calls listen()) or initiate
    # a connection to a target (run() calls send()).

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    # Define a method named 'send' within NetCat class.
    def send(self):
        # Connect to a socket using the target IP and port specified in 'args'.
        self.socket.connect((self.args.target, self.args.port))
        # If there's content in 'buffer', send it over the socket.
        if self.buffer:
            self.socket.send(self.buffer)
        # Start an infinite loop to receive responses from the server.
        try:
            while True:
                # Initialize variables for receiving data.
                recv_len = 1
                response = ''
                # Loop until no more data is received.
                while recv_len:
                    # Receive up to 4096 bytes of data from the socket.
                    data = self.socket.recv(4096)
                    # Update the length of received data.
                    recv_len = len(data)
                    # Append the received data to the response string.
                    response += data.decode()
                    # Break the loop if less than 4096 bytes were received, indicating the end of the message.
                    if recv_len < 4096:
                        break
                    # Print the response if it's not empty.
                    if response:
                        print(response)
                        # Prompt for user input and append a newline character.
                        buffer = input('> ')
                        buffer += '\n'
                        # Send the user input back to the server.
                        self.socket.send(buffer.encode())
        # Handle keyboard interrupt gracefully.
        except KeyboardInterrupt:
            print('User terminated.')
            # Close the socket connection.
            self.socket.close()
            # Exit the program.
            sys.exit()

    # Define a method named 'listen' within NetCat class.
    def listen(self):
        # Bind the socket to the target IP and port specified in 'args'.
        self.socket.bind((self.args.target, self.args.port))
        # Set the socket to listen mode with a backlog of 5 connections.
        self.socket.listen(5)
        # Infinite loop to accept incoming connections.
        while True:
            # Accept a new connection and create a client socket object.
            client_socket, _ret_address = self.socket.accept()
            print(_ret_address)
            # Create a new thread to handle the client connection.
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            # Start the client handling thread.
            client_thread.start()

    # Define a method named 'handle' within NetCat class.
    def handle(self, client_socket):
        # Check if the 'execute' argument is set.
        if self.args.execute:
            # Execute the specified command and send its output to the client.
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        # Check if the 'upload' argument is set.
        elif self.args.upload:
            # Receive the file data from the client and save it to a file.
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            # Send a confirmation message to the client.
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        # Check if the 'command' argument is set.
        elif self.args.command:
            # Handle command execution from the client.
            cmd_buffer = b''
            while True:
                try:
                    # Send a prompt to the client.
                    client_socket.send(b'BHP: #> ')
                    # Receive the command from the client until a newline is encountered.
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    # Execute the received command and send its output to the client.
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    # Reset the command buffer.
                    cmd_buffer = b''
                except Exception as e:
                    # Log any exceptions and terminate the program.
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

# Main entry point of the script.
if __name__ == '__main__':
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description='BHP Net Tool', formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(...))
    # Add command-line arguments.
    parser.add_argument('-c', '--command', action='store_true', help='command shell') 
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    # Parse the arguments.
    args = parser.parse_args()
    # Determine whether to read from stdin or start listening based on arguments.
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    # Instantiate the NetCat class with the parsed arguments and buffer.
    nc = NetCat(args, buffer.encode())
    # Run the NetCat instance.
    nc.run()
