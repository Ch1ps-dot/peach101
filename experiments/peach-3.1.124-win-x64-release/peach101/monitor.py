import psock, socket

def check_alive():
    try:
        sock = psock.ctsocket()
        sock.pconnect('127.0.0.1', 12345)
    except socket.error as e:
        exit(-1)

if __name__ == "__main__":
    check_alive()