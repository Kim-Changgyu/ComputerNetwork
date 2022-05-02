from socket import *

# Server Settings
HOST = "127.0.0.1"
PORT = 80

# Client Settings
USER_AGENT = "Python Socket Program Client"

# Create Request header
def MAKE_HEADER(method, url, version):
    header = "%s %s %s\r\n" % (method, url, version)
    header += "Host: %s:%d\r\n" % (HOST, PORT)
    header += "Content-Type: text/plain\r\n"
    header += "User-Agent: %s\r\n" % (USER_AGENT)
    header += "Connection: keep-alive\r\n\r\n"
    return header


# Loop
while True:
    # Initialize Client Socket
    CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCKET.connect((HOST, PORT))
    
    # Input Request line
    METHOD = input("METHOD >> ")
    URL = input("URL >> ")
    VERSION = input("HTTP VERSION >> ")
    
    # METHOD
    if METHOD == "EXIT":
        CLIENT_SOCKET.close()
        break
    elif METHOD == "POST":
        REQUEST_BODY = input("MESSAGE >> ")
    else:
        REQUEST_BODY = ""
    
    REQUEST_HEADERS = MAKE_HEADER(METHOD, URL, VERSION)
    
    REQUEST = REQUEST_HEADERS + REQUEST_BODY
    
    CLIENT_SOCKET.sendall(REQUEST.encode())
    
    RAW_RESPONSE = CLIENT_SOCKET.recv(65535)
    print(RAW_RESPONSE.decode())
    
    CLIENT_SOCKET.close()