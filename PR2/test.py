import socket
import threading
import random
import time

# Global lock to ensure thread-safe file access
file_lock = threading.Lock()

# Path to the file that will be operated on
file_path = "shared_file.txt"

# Function to handle a client's request
def handle_client(client_socket, client_address):
    try:
        print(f"Connected to {client_address}")

        # Read the incoming message from the client
        message = client_socket.recv(1024).decode("utf-8")
        if not message:
            return

        # Random sleep between 1 and 7 seconds to simulate delay
        sleep_time = random.randint(1, 7)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

        # Parse the command
        command_parts = message.split(" ", 1)
        command = command_parts[0]

        # Perform actions based on command type (read/write)
        if command == "write":
            data = command_parts[1] if len(command_parts) > 1 else ""
            write_to_file(data)
            client_socket.send("Write operation completed.".encode("utf-8"))
        elif command == "read":
            data = read_from_file()
            client_socket.send(data.encode("utf-8"))
        else:
            client_socket.send("Invalid command.".encode("utf-8"))

    except Exception as e:
        print(f"Error handling request from {client_address}: {e}")
        client_socket.send("Error processing request.".encode("utf-8"))
    finally:
        # Close the client connection
        client_socket.close()

# Function to write data to the file with locking
def write_to_file(data):
    with file_lock:
        with open(file_path, "a") as file:
            file.write(f"{data}\n")
        print(f"Data written: {data}")

# Function to read data from the file with locking
def read_from_file():
    with file_lock:
        try:
            with open(file_path, "r") as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return "File not found."

# Function to start the TCP server
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Max number of connections to wait for

    print(f"Server started on {host}:{port}")

    # Accept client connections in a loop
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    host = "127.0.0.1"  # Localhost
    port = 65432  # Arbitrary non-privileged port

    # Start the server
    start_server(host, port)
