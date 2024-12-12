import os, sys, socket
import psock

def pong():
    msock = psock.ctsocket()
    msock.pbind()
    msock.plisten()
     
    while(True):
        ct, addr = msock.paccept()
        recv = ct.recv(1024)
        print(f"receive: {recv}")
        if recv == b"ping":
            print("pong")
            print("pwn!")
            sys.exit(1)


if __name__ == "__main__":
    pong()