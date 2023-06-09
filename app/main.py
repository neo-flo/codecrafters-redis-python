# Uncomment this to pass the first stage
# import socket
import socket
import threading
import time

storage = {}


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
                key = commands[1]
                value_with_expiry = storage.get(key)
                if value_with_expiry is None:
                    send_response(self.client_socket, None)
                else:
                    value, expiry_time = value_with_expiry
                    if expiry_time is not None and expiry_time < time.time():
                        del storage[key]
                        send_response(self.client_socket, None)
                    else:
                        send_response(self.client_socket, value)
            elif commands[0].lower() == 'set':
                key = commands[1]
                value = commands[2]
                expiry_milliseconds = None

                if len(commands) > 3 and commands[-2].lower() == 'px':
                    expiry_milliseconds = int(commands[-1])
                if expiry_milliseconds is not None:
                    expiry_time = time.time() + (expiry_milliseconds / 1000.0)
                    storage[key] = (value, expiry_time)
                else:
                    storage[key] = (value, None)
                send_response(self.client_socket, 'OK')


if __name__ == "__main__":
    main()
