import socket

def localIP():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("Hostname:", hostname)
    print("IP Address:", ip_address)
    return ip_address