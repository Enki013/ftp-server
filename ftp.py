import os
import socket
import threading
from ftplib import FTP, error_perm

class FTPHandler(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        self.connection.send('220 Welcome to the FTP server\r\n')
        while True:
            try:
                command = self.connection.recv(1024).strip()
            except socket.error as err:
                print(f'Error reading from socket: {err}')
                break
            if not command:
                break
            try:
                cmd, arg = command.decode().split(' ', 1)
            except ValueError:
                cmd = command.decode()
                arg = ''
            func = getattr(self, f'ftp_{cmd.lower()}', None)
            if not func:
                self.connection.send(f'502 Command "{cmd}" not implemented\r\n'.encode())
            else:
                try:
                    response = func(arg)
                    self.connection.send(response.encode())
                except Exception as err:
                    print(f'Error executing command "{cmd}": {err}')
                    self.connection.send(f'500 Internal server error\r\n'.encode())
        self.connection.close()

    def ftp_user(self, username):
        return '331 OK\r\n'

    def ftp_pass(self, password):
        return '230 OK\r\n'

    def ftp_cwd(self, path):
        try:
            os.chdir(path)
            return f'250 CWD successful. "{os.getcwd()}" is current directory\r\n'
        except OSError:
            return '550 Failed to change directory\r\n'

    def ftp_pwd(self, _):
        return f'257 "{os.getcwd()}" is current directory\r\n'

    def ftp_list(self, _):
        files = os.listdir('.')
        return '\r\n'.join(files) + '\r\n'

    def ftp_pasv(self, _):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        s.listen(1)
        port = s.getsockname()[1]
        ip = socket.gethostbyname(socket.gethostname())
        return f'227 Entering Passive Mode ({",".join(ip.split("."))},{port//256},{port%256})\r\n'

    def ftp_retr(self, filename):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            return f'150 Opening binary mode data connection for "{filename}"\r\n{data}\r\n226 Transfer complete\r\n'
        except FileNotFoundError:
            return f'550 Failed to open file "{filename}"\r\n'
        except Exception as err:
            print(f'Error sending file "{filename}": {err}')
            return '500 Internal server error\r\n'

def main():
    host = 'localhost'
    port = 2121
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f'Server listening on {host}:{port}')
    while True:
        try:
            connection, address = server.accept()
            print(f'Accepted connection from {address}')
            handler = FTPHandler(connection)
            handler.start()
        except KeyboardInterrupt:
            break
    server.close()
    print('Server stopped')

if __name__ == '__main__':
    main()