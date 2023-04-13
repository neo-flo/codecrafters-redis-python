# Uncomment this to pass the first stage
# import socket
import socket
import threading


dict = {}
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379))

    while True:
        # accept connection
        (client_socket, address) = server_socket.accept()
        HandleRedisCommand(client_socket).start()


def send_response(client_socket, value):
    if not value:
        client_socket.sendall(b'$-1\r\n')
        return

    response = '+{}\r\n'.format(value)
    client_socket.sendall(response.encode('utf-8'))


class HandleRedisCommand(threading.Thread):
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

            commands = []
            lines = request.splitlines()
            for i in range(1, len(lines), 2):
                command = lines[i + 1]
                commands.append(command)
                print(f"Command {i // 2 + 1}: {command}")

            if commands[0].lower() == 'ping':
                send_response(self.client_socket, 'PONG')
            elif commands[-1].lower() == 'docs':
                send_response(self.client_socket, '')
            elif commands[0].lower() == 'echo':
                send_response(self.client_socket, commands[-1])
            elif commands[0].lower() == 'get':
                send_response(self.client_socket, dict.get(commands[1]))
            elif commands[0].lower() == 'set':
                dict[commands[1]] = commands[2]
                send_response(self.client_socket, 'OK')



if __name__ == "__main__":
    main()
