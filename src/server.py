from socket import *
from datetime import datetime

# Message List
MESSAGE = []

# Server Settings
SERVER_NAME = "Python Socket Program Server"
HOST = "127.0.0.1"
PORT = 80
DEBUG = True

# Initialize Server Socket
SERVER_SOCKET = socket(AF_INET, SOCK_STREAM)
SERVER_SOCKET.bind((HOST, PORT))
SERVER_SOCKET.listen(0)

# Create Response header
def MAKE_HEADER(version, status, name):
    header = "%s %s\r\n" % (version, status)
    header += "Server: %s\r\n" % (name)
    header += "Date: %s\r\n" % (datetime.now().strftime("%a, %d %b %Y %H:%M:%S KST"))
    header += "Content-Type: text/plain\r\n"
    header += "Connection: keep-alive\r\n\r\n"
    return header
            
            
CLIENT_SOCKET, ADDR = None, None

# Loop
while True:
    if CLIENT_SOCKET:
        CLIENT_SOCKET.close()
    
    CLIENT_SOCKET, ADDR = SERVER_SOCKET.accept()

    RAW_REQUEST = CLIENT_SOCKET.recv(65535)
    
    # Connection Closing Request From Client
    if RAW_REQUEST.decode() == "":
        break
    
    # Decode
    REQUEST = RAW_REQUEST.decode().split("\r\n")
    
    if DEBUG:
        for line in REQUEST:
            print(line)
            
    METHOD, URL, VERSION = REQUEST[0].split()[0], REQUEST[0].split()[1], REQUEST[0].split()[2]
    
    try:
        if METHOD == "GET":
            if URL[0] == "/" and URL.count("/") == 1:
                STATUS_CODE = "200 OK"

                # BODY
                RESPONSE_BODY = "HTTP %s Method (Success)\r\n\r\n" % (METHOD)
                for line in MESSAGE:
                    RESPONSE_BODY += "%s\r\n" % (line)
            else:
                STATUS_CODE = "404 Not Found"

                # BODY
                RESPONSE_BODY = "HTTP %s Method (Failed)\r\n" % (METHOD)
        elif METHOD == "POST":
            # Finding BODY
            for i, line in enumerate(REQUEST):
                if line == "":
                    BODY = REQUEST[i+1:]
                    
            if URL == "/":
                STATUS_CODE = "201 Created"

                # BODY
                RESPONSE_BODY = "HTTP %s Method (Success)\r\n\r\n" % (METHOD)
                for line in BODY:
                    MESSAGE.append(line)
                    RESPONSE_BODY += "%s\r\n" % (line)
            else:
                STATUS_CODE = "404 Not Found"
            
                # BODY
                RESPONSE_BODY = "HTTP %s Method (Failed)\r\n" % (METHOD)
        elif METHOD == "DELETE":
            MESSAGE.clear()
            
            STATUS_CODE = "200 OK"
        
            # BODY
            RESPONSE_BODY = "HTTP DELETE Method (Success)\r\n"
        else:
            STATUS_CODE = "405 Method Not Allowed"
        
            # BODY
            RESPONSE_BODY = "HTTP %s Method (Failed)\r\n" % (METHOD)
    except Exception as e:
        STATUS_CODE = "500 Internal Server Error"
        
        # BODY
        RESPONSE_BODY = "HTTP %s Method (Failed)\r\n" % (METHOD)
        
    # RESPONSE HEADERS
    RESPONSE_HEADERS = MAKE_HEADER(version=VERSION, status=STATUS_CODE, name=SERVER_NAME)
    
    RESPONSE = RESPONSE_HEADERS + RESPONSE_BODY
        
    CLIENT_SOCKET.sendall(RESPONSE.encode())

CLIENT_SOCKET.close()
SERVER_SOCKET.close()