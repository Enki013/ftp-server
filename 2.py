
# from pyftpdlib.authorizers import DummyAuthorizer
# from pyftpdlib.handlers import FTPHandler
# from pyftpdlib.servers import FTPServer

# FTP_USERNAME = 'anonymous'
# FTP_PASSWORD = '12345'
# FTP_DIRECTORY = 'C:/FTP'

# # Set up authorizer with a single user
# authorizer = DummyAuthorizer()
# authorizer.add_user(FTP_USERNAME, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmwMT')

# # Set up FTP handler with passive ports range
# handler = FTPHandler
# handler.passive_ports = range(60000, 65535)

# # Set up FTP server with authorizer and handler
# server = FTPServer(('0.0.0.0', 2121), handler)
# server.authorizer = authorizer

# # Start the server
# server.serve_forever()
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

# define the root directory for the FTP server
root_dir = "\\"

# define the FTP handler class
class CustomFTPHandler(FTPHandler):

    # override the on_file_received method to set file permissions
    def on_file_received(self, file):
        file_path = os.path.abspath(self.fs.ftp2fs(file))
        os.chmod(file_path, 0o666)

# create the dummy authorizer
authorizer = DummyAuthorizer()

# set the root directory for the FTP server
authorizer.add_anonymous(root_dir)

# create the FTP server
ftp_server = FTPServer(('127.0.0.1', 21), CustomFTPHandler)

# set the authorizer for the FTP server
ftp_server.handler.authorizer = authorizer

# start the FTP server
ftp_server.serve_forever()