from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_DIRECTORY = 'C:/FTP'
FTP_ADDRESS = '127.0.0.1'
FTP_PORT = 21

def start_server():
    # set up FTP handler with passive ports range and file sharing enabled
    handler = FTPHandler
    handler.authorizer = None
    handler.passive_ports = range(60000, 65535)
    handler.permit_foreign_addresses = True
    handler.banner = "Welcome to my FTP server"

    # set up FTP server with handler and address
    server = FTPServer((FTP_ADDRESS, FTP_PORT), handler)

    # start the server
    server.serve_forever()

if __name__ == '__main__':
    start_server()