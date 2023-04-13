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
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def run(self) -> None:
        print('-------------------------------------')
        print('client connected\n')

        while True:
            request = self.client_socket.recv(1024).decode('utf-8')
            print('request : ' + request)

            if not request:
                print('client disconnected\n')
                self.client_socket.close()
                break

            for line in request.splitlines():
                print('line : ' + line)
                if line == 'ping':
                    self.client_socket.sendall(b'+PONG\r\n')
                elif line == 'DOCS':
                    self.client_socket.sendall(b'+\r\n')


if __name__ == "__main__":
    main()
