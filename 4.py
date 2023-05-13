import ftplib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Set up the FTP server parameters
FTP_ADDRESS = "localhost"
FTP_PORT = 21
FTP_USER = "username"
FTP_PASSWORD = "password"
FTP_DIRECTORY = "/"

def start_ftp_server():
    # Create a dummy authorizer for managing FTP users and permissions
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmwMT')

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Set up the FTP server and start it
    ftp_server = FTPServer((FTP_ADDRESS, FTP_PORT), handler)
    ftp_server.serve_forever()

if __name__ == '__main__':
    start_ftp_server()