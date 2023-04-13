# Uncomment this to pass the first stage
# import socket
import socket
import threading


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379))

    while True:
        # accept connection
        (client_socket, address) = server_socket.accept()
        RedisCommand(client_socket).start()


class RedisCommand(threading.Thread):
    def __init__(self, client_socket):
        print('client connected')
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self) -> None:
        output = "+PONG\r\n"
        self.client_socket.send(output.encode('ascii'))

        if self.client_socket is not None:
            self.client_socket.close()


if __name__ == "__main__":
    main()
