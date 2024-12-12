import socket

class ctsocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def pconnect(self, host, port):
        return self.sock.connect((host, port))

    def psend(self, msg):
        return self.sock.send(msg)

    def pbind(self):
        return self.sock.bind(('127.0.0.1', 12345))

    def plisten(self):
        return self.sock.listen(5)

    def paccept(self):
        return self.sock.accept()

    def precv(self, buff):
        chunk = self.sock.recv(buff)
        return chunk