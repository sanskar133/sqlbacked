import socket

def send_message_to_server(host, port, message):
    """
    Connects to a socket server and sends a message.

    Args:
        host (str): The hostname or IP address of the server.
        port (int): The port number the server is listening on.
        message (str): The message to send.
    """
    try:
        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Encode the message and send it
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent message: '{message}'")

        # Optionally, receive a response from the server
        data = client_socket.recv(1024)  # Receive up to 1024 bytes
        if data:
            print(f"Received from server: '{data.decode('utf-8')}'")

    except ConnectionRefusedError:
        print(f"Connection refused. Ensure the server is running on {host}:{port}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if 'client_socket' in locals() and client_socket:
            client_socket.close()
            print("Connection closed.")

if __name__ == "__main__":
    SERVER_HOST = "0.0.0.0"  # Or the actual IP address of your server
    SERVER_PORT = 5000       # The port your server is listening on
    MESSAGE_TO_SEND = "Hello from the Python client!"

    send_message_to_server(SERVER_HOST, SERVER_PORT, MESSAGE_TO_SEND)